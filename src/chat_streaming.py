from dataclasses import dataclass
import json
import logging
import os
import requests
import time

from tabulate import tabulate
from dotenv import load_dotenv
import tiktoken

load_dotenv()

api_key = os.getenv("APIM_KEY")
api_endpoint = os.getenv("APIM_ENDPOINT")
chat_deployment_name = os.getenv("DEPLOYMENT_NAME")
sleep_time = float(os.getenv("SLEEP_TIME", "0"))
table_format = os.getenv("TABLE_FORMAT", "github")

if api_key is None:
    print("APIM_KEY is not set")
    exit(1)
if api_endpoint is None:
    print("APIM_ENDPOINT is not set")
    exit(1)
if chat_deployment_name is None:
    print("CHAT_DEPLOYMENT_NAME is not set")
    exit(1)


def num_tokens_from_string(string: str, model: str) -> int:
    """Returns the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logging.warning("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def read_events(response: requests.Response):
    def strip_data_prefix(data):
        if data.startswith("data: "):
            return data[6:]
        return data

    event_buffer: str = ""
    for chunk in response:
        # convert to string and add to buffer
        decoded_chunk = chunk.decode("utf-8")
        event_buffer += decoded_chunk
        # yield any complete events
        while "\n\n" in event_buffer:
            tmp_event, event_buffer = event_buffer.split("\n\n", 1)
            yield strip_data_prefix(tmp_event)

    # yield any remaining buffer
    if event_buffer:
        yield strip_data_prefix(event_buffer)


@dataclass
class RequestSummary:
    status_code: int
    text: str
    num_chunks: int
    apim1_tokens_remaining: int
    apim1_tokens_consumed: int
    apim2_tokens_remaining: int
    apim2_tokens_consumed: int
    rate_limit_remaining_tokens: int | None
    rate_limit_remaining_requests: int | None
    body_tokens_prompt: int | None
    body_tokens_completion: int | None
    body_tokens_total: int | None


def call_chat_api_streaming():
    url = f"{api_endpoint}/openai/deployments/{chat_deployment_name}/chat/completions"
    querystring = {"api-version": "2024-02-15-preview"}

    payload = (
        '{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": true,"max_tokens": 100}'
    )
    headers = {
        "content-type": "application/json",
        "api-key": api_key,
        "ocp-apim-subscription-key": api_key,
    }

    # print(f"Connnecting to {url}")

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, stream=True, timeout=10)

    # print(response.headers)
    # print("---")

    result = ""
    num_chunks = 0
    for event in read_events(response):
        if event != "[DONE]":
            # print(event)
            completion_chunk = json.loads(event)
            choices = completion_chunk.get("choices")
            if choices and len(choices) > 0:
                result += choices[0]["delta"].get("content") or ""
                num_chunks += 1

    apim1_tokens_remaining = int(response.headers["x-apim1-tokens-remaining"])
    apim1_tokens_consumed = int(response.headers["x-apim1-tokens-consumed"])
    apim2_tokens_remaining = int(response.headers["x-apim2-tokens-remaining"])
    apim2_tokens_consumed = int(response.headers["x-apim2-tokens-consumed"])
    rate_limit_remaining_tokens = int(response.headers["x-ratelimit-remaining-tokens"])
    rate_limit_remaining_requests = int(response.headers["x-ratelimit-remaining-requests"])

    calculated_completion_tokens = num_tokens_from_string(result, "gpt-3.5-turbo-0613")

    return RequestSummary(
        status_code=response.status_code,
        text=result,
        num_chunks=num_chunks,
        apim1_tokens_remaining=apim1_tokens_remaining,
        apim1_tokens_consumed=apim1_tokens_consumed,
        apim2_tokens_remaining=apim2_tokens_remaining,
        apim2_tokens_consumed=apim2_tokens_consumed,
        rate_limit_remaining_tokens=rate_limit_remaining_tokens,
        rate_limit_remaining_requests=rate_limit_remaining_requests,
        body_tokens_prompt=None,
        body_tokens_completion=None,
        body_tokens_total=None,
    )




def test_chat_streaming():
    print(f"Running chat streaming test ({api_endpoint})")
    
    results = []
    for i in range(10):
        print(f"Making request {i}...")
        result = call_chat_api_streaming()
        results.append(result)
        if sleep_time > 0:
            time.sleep(sleep_time)

    last_apim_tokens_remaining = -1
    last_rate_limit_tokens_remaining = -1
    table_data = []
    for r in results:
        table_data.append(
            [
                r.status_code,
                r.apim1_tokens_remaining,
                r.apim1_tokens_consumed,
                last_apim_tokens_remaining - r.apim1_tokens_remaining if last_apim_tokens_remaining >= 0 else "n/a",
                # r.apim2_tokens_consumed,
                # r.apim2_tokens_remaining,
                r.rate_limit_remaining_tokens,
                (
                    last_rate_limit_tokens_remaining - r.rate_limit_remaining_tokens
                    if last_rate_limit_tokens_remaining >= 0
                    else "n/a"
                ),
                r.rate_limit_remaining_requests,
                num_tokens_from_string(r.text, "gpt-3.5-turbo-0613"),
            ]
        )
        last_apim_tokens_remaining = r.apim1_tokens_remaining
        last_rate_limit_tokens_remaining = r.rate_limit_remaining_tokens

    columns = [
        "Status code",
        "APIM tokens remaining",
        "APIM tokens consumed",
        "APIM tokens remaining (delta)",
        "Rate limit tokens remaining",
        "Rate limit tokens remaining (delta)",
        "Rate limit requests remaining",
        "Tiktoken count (generated)",
    ]

    print(tabulate(table_data, columns, tablefmt=table_format))


test_chat_streaming()
