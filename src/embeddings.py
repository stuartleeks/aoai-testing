from dataclasses import dataclass
import json
import math
import os
import requests
import time

from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("APIM_KEY")
api_endpoint = os.getenv("APIM_ENDPOINT")
embedding_deployment_name = os.getenv("EMBEDDING_DEPLOYMENT_NAME")
sleep_time = float(os.getenv("SLEEP_TIME", "0"))
table_format = os.getenv("TABLE_FORMAT", "github")
request_count = int(os.getenv("REQUEST_COUNT", "10"))

if api_key is None:
    print("APIM_KEY is not set")
    exit(1)
if api_endpoint is None:
    print("APIM_ENDPOINT is not set")
    exit(1)
if embedding_deployment_name is None:
    print("EMBEDDING_DEPLOYMENT_NAME is not set")
    exit(1)


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
    predicted_token_delta: int


def call_embedding_api_non_streaming():
    url = f"{api_endpoint}/openai/deployments/{embedding_deployment_name}/embeddings"
    querystring = {"api-version": "2024-02-15-preview"}

    # payload = '{"input": "This is some text to generate embeddings for", "model": "embedding"}'
    # payload = (
    #     '{"input": "This is some text to generate embeddings for and is'
    #     + ' longer than the previous text which really was quite short.'
    #     + ' This would be a good place to put a short story about a dog.'
    #     + ' I mean, who doesn''t like stories about dogs?", "model": "embedding"}'
    # )
    # payload = (
    #     '{"input": "This is some text to generate embeddings for and is'
    #     + ' longer than the previous text which really was quite short.'
    #     + ' This would be a good place to put a short story about a dog.'
    #     + ' I mean, who doesn''t like stories about dogs?'
    #     + ' There was a dog called Alberta who love to go for walks in the park.'
    #     + ' She was a very good dog and loved to play with other dogs.'
    #     + ' She was a very friendly dog and loved to play with children.'
    #     + ' She was a very happy dog and loved to play with her toys.'
    #     + ' She was a very playful dog and loved to play with her owner.'
    #     + '", "model": "embedding"}'
    # )
    payload = (
        '{"input": "This is some text to generate embeddings for and is'
        + ' longer than the previous text which really was quite short.'
        + ' This would be a good place to put a short story about a dog.'
        + ' I mean, who doesn''t like stories about dogs?'
        + ' There was a dog called Alberta who love to go for walks in the park.'
        + ' She was a very good dog and loved to play with other dogs.'
        + ' She was a very friendly dog and loved to play with children.'
        + ' She was a very happy dog and loved to play with her toys.'
        + ' She was a very playful dog and loved to play with her owner.'
        + ' Every day, Alberta would go for a walk in the park.'
        + ' She would run around and play with other dogs.'
        + ' She would chase after squirrels and birds.'
        + ' She would roll around in the grass and dirt.'
        + ' She would jump up and down and bark.'
        + ' She would wag her tail and lick her owner.'
        + ' She would fetch sticks and balls.'
        + '", "model": "embedding"}'
    )
    # payload = (
    #     '{"input": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Pellentesque pulvinar pellentesque habitant morbi tristique senectus et netus et. Diam quis enim lobortis scelerisque. Semper risus in hendrerit gravida rutrum quisque. Lobortis feugiat vivamus at augue eget arcu dictum. Pellentesque elit eget gravida cum sociis natoque penatibus et magnis. Massa sapien faucibus et molestie ac feugiat sed lectus vestibulum. Id leo in vitae turpis massa sed. Vitae aliquet nec ullamcorper sit amet. Enim nunc faucibus a pellentesque sit amet porttitor eget dolor. Vitae ultricies leo integer malesuada. Viverra accumsan in nisl nisi. Massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada proin. Mi quis hendrerit dolor magna eget est lorem ipsum. Convallis convallis tellus id interdum. Netus et malesuada fames ac turpis egestas sed tempus. Purus gravida quis blandit turpis cursus in hac habitasse. Nunc id cursus metus aliquam. Facilisis leo vel fringilla est ullamcorper eget nulla facilisi. Venenatis lectus magna fringilla urna porttitor rhoncus dolor. Et netus et malesuada fames ac turpis egestas. Donec et odio pellentesque diam volutpat commodo sed. Lacus sed turpis tincidunt id aliquet risus feugiat in ante. Est ullamcorper eget nulla facilisi etiam dignissim. Nisl nunc mi ipsum faucibus vitae. At in tellus integer feugiat. Velit aliquet sagittis id consectetur. Velit sed ullamcorper morbi tincidunt. Consectetur libero id faucibus nisl tincidunt eget nullam non nisi. At imperdiet dui accumsan sit amet nulla facilisi morbi. In est ante in nibh mauris cursus. Dignissim convallis aenean et tortor at. Donec adipiscing tristique risus nec. Mi in nulla posuere sollicitudin. Dui sapien eget mi proin sed libero enim sed faucibus. Felis eget velit aliquet sagittis id consectetur purus. Ullamcorper malesuada proin libero nunc consequat. Integer malesuada nunc vel risus commodo viverra maecenas. Aliquam ut porttitor leo a diam sollicitudin. Congue quisque egestas diam in. Blandit massa enim nec dui nunc mattis enim ut. Id neque aliquam vestibulum morbi blandit cursus risus at. Nisi scelerisque eu ultrices vitae auctor eu augue ut lectus. Enim nulla aliquet porttitor lacus luctus accumsan tortor. Praesent elementum facilisis leo vel. Arcu dui vivamus arcu felis bibendum ut tristique. Ut tristique et egestas quis ipsum suspendisse ultrices gravida dictum. Id leo in vitae turpis massa sed. Pretium nibh ipsum consequat nisl vel. Ante in nibh mauris cursus. Viverra justo nec ultrices dui sapien eget mi. Amet massa vitae tortor condimentum lacinia quis vel. Quis imperdiet massa tincidunt nunc. Auctor neque vitae tempus quam pellentesque nec. Convallis posuere morbi leo urna. Ullamcorper morbi tincidunt ornare massa eget egestas. Neque aliquam vestibulum morbi blandit cursus risus at ultrices. Est placerat in egestas erat imperdiet sed euismod nisi porta. Blandit volutpat maecenas volutpat blandit aliquam etiam erat velit. Libero id faucibus nisl tincidunt eget nullam non nisi est. Amet risus nullam eget felis eget. Tristique senectus et netus et malesuada fames ac turpis. Ac orci phasellus egestas tellus rutrum tellus pellentesque eu tincidunt. Turpis nunc eget lorem dolor sed.", "model": "embedding"}'
    # )

    headers = {
        "content-type": "application/json",
        "api-key": api_key,
        "ocp-apim-subscription-key": api_key,
    }

    response = requests.request(
        "POST", url, data=payload, headers=headers, params=querystring, timeout=10
    )

    success = response.status_code < 300
    
    print(len(json.loads(payload)["input"]))
    print(len(payload) - len(json.loads(payload)["input"]))

    predicted_token_delta = math.ceil(len(json.loads(payload)["input"])*0.25)
    apim1_tokens_remaining = int(response.headers["x-apim1-tokens-remaining"])
    apim1_tokens_consumed = int(response.headers["x-apim1-tokens-consumed"])
    apim2_tokens_remaining = int(response.headers["x-apim2-tokens-remaining"])
    apim2_tokens_consumed = int(response.headers["x-apim2-tokens-consumed"])

    rate_limit_remaining_tokens = (
        int(response.headers["x-ratelimit-remaining-tokens"]) if success else None
    )
    rate_limit_remaining_requests = (
        int(response.headers["x-ratelimit-remaining-requests"]) if success else None
    )

    if success:
        body = response.json()
        body_tokens_prompt = body["usage"]["prompt_tokens"]
        body_tokens_completion = None
        # body_tokens_completion = body["usage"]["completion_tokens"]
        body_tokens_total = body["usage"]["total_tokens"]
    else:
        body_tokens_prompt = None
        body_tokens_completion = None
        body_tokens_total = None

    return RequestSummary(
        status_code=response.status_code,
        text="",
        num_chunks=1,
        apim1_tokens_remaining=apim1_tokens_remaining,
        apim1_tokens_consumed=apim1_tokens_consumed,
        apim2_tokens_remaining=apim2_tokens_remaining,
        apim2_tokens_consumed=apim2_tokens_consumed,
        rate_limit_remaining_tokens=rate_limit_remaining_tokens,
        rate_limit_remaining_requests=rate_limit_remaining_requests,
        body_tokens_prompt=body_tokens_prompt,
        body_tokens_completion=body_tokens_completion,
        body_tokens_total=body_tokens_total,
        predicted_token_delta=predicted_token_delta,
    )


def test_embedding_non_streaming():
    print(f"Running embededing non-streaming test ({api_endpoint})")

    results = []
    for i in range(request_count):
        print(f"Making request {i}...")
        result = call_embedding_api_non_streaming()
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
                (
                    last_apim_tokens_remaining - r.apim1_tokens_remaining
                    if last_apim_tokens_remaining >= 0
                    else "n/a"
                ),
                r.rate_limit_remaining_tokens,
                (
                    last_rate_limit_tokens_remaining - r.rate_limit_remaining_tokens
                    if last_rate_limit_tokens_remaining >= 0
                    and r.rate_limit_remaining_tokens is not None
                    else "n/a"
                ),
                r.predicted_token_delta,
                r.body_tokens_prompt,
            ]
        )
        last_apim_tokens_remaining = r.apim1_tokens_remaining or -1
        last_rate_limit_tokens_remaining = r.rate_limit_remaining_tokens or -1

    columns = [
        "Status code",
        "APIM tokens remaining",
        "APIM tokens consumed",
        "APIM tokens remaining (delta)",
        "Rate limit tokens remaining",
        "Rate limit tokens remaining (delta)",
        "Predicted token delta",
        "Body tokens (prompt)",
    ]

    print(tabulate(table_data, columns, tablefmt=table_format))


test_embedding_non_streaming()
