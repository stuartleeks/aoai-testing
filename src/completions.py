from dataclasses import dataclass
import datetime
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
copmletions_deployment_name = os.getenv("DEPLOYMENT_NAME")
sleep_time = float(os.getenv("SLEEP_TIME", "0"))
table_format = os.getenv("TABLE_FORMAT", "github")
request_count = int(os.getenv("REQUEST_COUNT", "10"))

if api_key is None:
    print("APIM_KEY is not set")
    exit(1)
if api_endpoint is None:
    print("APIM_ENDPOINT is not set")
    exit(1)
if copmletions_deployment_name is None:
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


@dataclass
class RequestSummary:
    status_code: int
    text: str
    num_chunks: int
    rate_limit_remaining_tokens: int | None
    rate_limit_remaining_requests: int | None
    body_tokens_prompt: int | None
    body_tokens_completion: int | None
    body_tokens_total: int | None


def call_completions_api_non_streaming():
    url = f"{api_endpoint}/openai/deployments/{copmletions_deployment_name}//completions"
    querystring = {"api-version": "2024-02-15-preview"}

    payload = (
        # '{"prompt": "What is the meaning of life?"}'
        '{"prompt": "I am in a philosophical yet optimistic mood and a friend asked me what I thought the meaning of life is. My response is"}'
        # '{"prompt": "What is the meaning of life?","max_tokens": 10}'
        # '{"prompt": "What is the meaning of life?","max_tokens": 100}'
        # '{"prompt": "What is the meaning of life?","max_tokens": 1000}'
        # '{"prompt": "What is the meaning of life?","max_tokens": 2000}'
    )

    headers = {
        "content-type": "application/json",
        "api-key": api_key,
        "ocp-apim-subscription-key": api_key,
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, timeout=30)

    success = response.status_code < 300

    rate_limit_remaining_tokens = int(response.headers["x-ratelimit-remaining-tokens"]) if success else None
    rate_limit_remaining_requests = int(response.headers["x-ratelimit-remaining-requests"]) if success else None

    if success:
        body = response.json()
        text = body["choices"][0]["text"]
        body_tokens_prompt = body["usage"]["prompt_tokens"]
        body_tokens_completion = body["usage"]["completion_tokens"]
        body_tokens_total = body["usage"]["total_tokens"]
    else:
        text = ""
        body_tokens_prompt = None
        body_tokens_completion = None
        body_tokens_total = None

    return RequestSummary(
        status_code=response.status_code,
        text=text,
        num_chunks=1,
        rate_limit_remaining_tokens=rate_limit_remaining_tokens,
        rate_limit_remaining_requests=rate_limit_remaining_requests,
        body_tokens_prompt=body_tokens_prompt,
        body_tokens_completion=body_tokens_completion,
        body_tokens_total=body_tokens_total,
    )


def test_completions_non_streaming():
    print(f"Running completions non-streaming test ({api_endpoint})")

    results = []
    for i in range(request_count):
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} Making request {i}...")
        result = call_completions_api_non_streaming()
        results.append(result)
        if sleep_time > 0:
            time.sleep(sleep_time)

    last_rate_limit_tokens_remaining = -1
    last_rate_limit_requests_remaining = -1
    table_data = []
    for r in results:
        table_data.append(
            [
                r.status_code,
                r.rate_limit_remaining_tokens,
                (
                    last_rate_limit_tokens_remaining - r.rate_limit_remaining_tokens
                    if last_rate_limit_tokens_remaining >= 0 and r.rate_limit_remaining_tokens is not None
                    else "n/a"
                ),
                r.rate_limit_remaining_requests,
                (
                    last_rate_limit_requests_remaining - r.rate_limit_remaining_requests
                    if last_rate_limit_requests_remaining >= 0 and r.rate_limit_remaining_requests is not None
                    else "n/a"
                ),
                num_tokens_from_string(r.text, "gpt-3.5-turbo-0613"),
                r.body_tokens_prompt,
                r.body_tokens_completion,
            ]
        )
        # last_apim_tokens_remaining = r.apim1_tokens_remaining or -1
        last_rate_limit_tokens_remaining = r.rate_limit_remaining_tokens or -1
        last_rate_limit_requests_remaining = r.rate_limit_remaining_requests or -1

    columns = [
        "Status code",
        "Rate limit tokens remaining",
        "Rate limit tokens remaining (delta)",
        "Rate limit requests remaining",
        "Rate limit requests remaining (delta)",
        "Tiktoken count (generated)",
        "Body tokens (prompt)",
        "Body tokens (completion)",
    ]

    print(tabulate(table_data, columns, tablefmt=table_format))


test_completions_non_streaming()
