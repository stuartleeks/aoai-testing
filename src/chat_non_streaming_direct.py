from dataclasses import dataclass
import datetime
import json
import logging
import os
import requests
import time

from tabulate import tabulate
from dotenv import load_dotenv
import tiktoken

load_dotenv()

api_key = os.getenv("API_KEY")
api_endpoint = os.getenv("APIM_ENDPOINT")
chat_deployment_name = os.getenv("DEPLOYMENT_NAME")
sleep_time = float(os.getenv("SLEEP_TIME", "0"))
table_format = os.getenv("TABLE_FORMAT", "github")
request_count = int(os.getenv("REQUEST_COUNT", "10"))

tiktoken_model = os.getenv("TIKTOKEN_MODEL", "gpt-3.5-turbo-0613")

if api_key is None:
    print("API_KEY is not set")
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
    payload_length: int | None


def call_chat_api_non_streaming():
    url = f"{api_endpoint}/openai/deployments/{chat_deployment_name}/chat/completions"
    querystring = {"api-version": "2024-02-15-preview"}

    payload = (
        # '{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false}'
        # '{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false,"max_tokens": 10}'
        # '{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false,"max_tokens": 100}'
        # '{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false,"max_tokens": 1000}'
        # '{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false,"max_tokens": 2000}'
        # '{"messages": [{"role": "user","content": "Imagine you are a school teacher and you have a room full of eight year old children. Your task is to get them excited and interested in science and today\'s topic is gravity. How would you explain gravity to captivate their interest?"}],"stream": false}'
        # '{"messages": [ {"role": "system","content": [{"type": "text","text": "You are an AI assistant that helps people find information."}]},{"role": "user","content": [{"type": "text","text": "What is gravity?"}]},{"role": "assistant","content": [{"type": "text","text": "Gravity is a fundamental force of nature that attracts two bodies towards each other. It is the force that causes objects to fall to the ground when dropped, and it keeps the planets in orbit around the Sun. The force of gravity is proportional to the mass of the objects and inversely proportional to the square of the distance between their centers. This concept was described by Isaac Newton in the 17th century with his law of universal gravitation. Later, Albert Einstein\'s theory of general relativity, proposed in the early 20th century, provided a deeper understanding by describing gravity not as a force, but as a curvature of spacetime caused by mass and energy."}]},{"role": "user","content": [{"type": "text","text": "Imagine you are a school teacher and you have a room full of eight year old children. Your task is to get them excited and interested in science and today\'s topic is gravity. How would you explain gravity to captivate their interest?"}]}],"stream": false}'
        # '{"messages": [ {"role": "system","content": [{"type": "text","text": "You are an AI assistant that helps people find information."}]},{"role": "user","content": [{"type": "text","text": "What is gravity?"}]},{"role": "assistant","content": [{"type": "text","text": "Gravity is a fundamental force of nature that attracts two bodies towards each other. It is the force that causes objects to fall to the ground when dropped, and it keeps the planets in orbit around the Sun. The force of gravity is proportional to the mass of the objects and inversely proportional to the square of the distance between their centers. This concept was described by Isaac Newton in the 17th century with his law of universal gravitation. Later, Albert Einstein\'s theory of general relativity, proposed in the early 20th century, provided a deeper understanding by describing gravity not as a force, but as a curvature of spacetime caused by mass and energy."}]},{"role": "user","content": [{"type": "text","text": "Imagine you are a school teacher and you have a room full of eight year old children. Your task is to get them excited and interested in science and today\'s topic is gravity. How would you explain gravity to captivate their interest?"}]},{"role": "assistant","content": [{"type": "text","text": "Alright, kids! Today we\'re going to talk about something super cool called gravity! Have you ever wondered why when you jump, you always come back down to the ground instead of floating away into the sky? Well, that's because of gravity!\n\nImagine gravity as a magical invisible force that pulls things together. It\'s like when you play with magnets – how they pull towards each other. Now, the Earth is like a giant magnet, but instead of pulling metal, it pulls everything towards it, including us!\n\nLet's do a fun experiment. Everyone, hold something small like a pencil or a toy. On the count of three, let\'s all drop them together. One, two, three, drop! Did you see that? Everything fell down! That happened because of gravity pulling them down to the ground.\n\nGuess what? Gravity is not just here on Earth. It\'s everywhere! It\'s the reason why the Moon goes around the Earth instead of flying off into space. It\'s also why we have tides in the ocean. The Moon's gravity pulls on the water.\n\nAnd here\'s a fun fact: even though gravity is pulling us down, we are also pulling the Earth up towards us! But because we are so much smaller than the Earth, we don\'t really move it. But it\'s still fun to think that we have our own little pull!\n\nSo remember, every time you jump and come back down, it's gravity at work, like a magic invisible string pulling you back to Earth. Isn't that fascinating?\n\nNow, let\'s watch a little video that shows astronauts in space. They float around because they are far from Earth, where gravity is much weaker. Watch how they move differently from us. It's really fun to see!\n\nBy understanding gravity, we learn more about how everything in the universe works together, from the smallest pebble to the biggest sun! Isn\'t science amazing? Let's explore more and keep asking questions. What do you want to know more about?"}]},{"role": "user","content": [{"type": "text","text": "What experiments might you do with them?"}]}],"stream": false}'
        """{
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are an AI assistant that helps people find information."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is gravity?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Gravity is a fundamental force of nature that attracts two bodies towards each other. It is the force that causes objects to fall to the ground when dropped, and it keeps the planets in orbit around the Sun. The force of gravity is proportional to the mass of the objects and inversely proportional to the square of the distance between their centers. This concept was described by Isaac Newton in the 17th century with his law of universal gravitation. Later, Albert Einstein's theory of general relativity, proposed in the early 20th century, provided a deeper understanding by describing gravity not as a force, but as a curvature of spacetime caused by mass and energy."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Imagine you are a school teacher and you have a room full of eight year old children. Your task is to get them excited and interested in science and today's topic is gravity. How would you explain gravity to captivate their interest?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Alright, kids! Today we're going to talk about something super cool called gravity! Have you ever wondered why when you jump, you always come back down to the ground instead of floating away into the sky? Well, that's because of gravity!"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What experiments might you do with them?"
        }
      ]
    }
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 800
}
"""

    )

    print(json.loads(payload))
    

    headers = {
        "content-type": "application/json",
        "api-key": api_key,
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring, timeout=30)

    success = response.status_code < 300
    print(response.text)

    rate_limit_remaining_tokens = int(response.headers["x-ratelimit-remaining-tokens"]) if success else None
    rate_limit_remaining_requests = int(response.headers["x-ratelimit-remaining-requests"]) if success else None

    if success:
        body = response.json()
        text = body["choices"][0]["message"]["content"]
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
        payload_length= len(payload)
    )


def test_chat_non_streaming():
    print(f"Running chat non-streaming test ({api_endpoint})")

    results = []
    for i in range(request_count):
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} Making request {i}...")
        result = call_chat_api_non_streaming()
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
                num_tokens_from_string(r.text, tiktoken_model),
                r.body_tokens_prompt,
                r.body_tokens_completion,
                r.payload_length
            ]
        )
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
        "Payload length"
    ]

    print(tabulate(table_data, columns, tablefmt=table_format))


test_chat_non_streaming()
