# token rate-limit decrement tests

- [token rate-limit decrement tests](#token-rate-limit-decrement-tests)
  - [Test setup](#test-setup)
  - [Summary](#summary)
  - [Requests](#requests)
    - [Request 1](#request-1)
    - [Request 2](#request-2)
    - [Request 3](#request-3)
    - [Request 4](#request-4)
    - [Request 5](#request-5)


## Test setup

- PAYG AOAI service.
- `gpt-3.5-turbo` model
- TPM quota of `10,000` TPM
- `max_tokens` not set
- non-streaming
- waited between each test to allow the rate limit to reset


## Summary

The summary of the test results is as follows:

| Request | Prompt tokens | Completion tokens | x-ratelimit-remaining-tokens delta |
| ------- | ------------- | ----------------- | ---------------------------------- |
| 1       | 15            | 96                | 16                                 |
| 2       | 36            | 213               | 16                                 |
| 3       | 21            | 105               | 16                                 |
| 4       | 145           | 180               | 16                                 |
| 5       | 914           | 101               | 16                                 |

Notes:
- regardless of the prompt and completion token count, the rate limit tokens remaining delta is always 16

## Requests

### Request 1

Request:
```json
{
  "messages": [{
    "role": "user",
    "content": "What is the meaning of life?"
    }],
  "model": "gpt-5-turbo-1"
}
```

Result

|                                      |     |
| ------------------------------------ | --- |
| `prompt_tokens`                      | 15  |
| `completion_tokens`                  | 96  |
| `x-ratelimit-remaining-tokens` delta | 16  |


### Request 2

Request:
```json
{
  "messages": [{
    "role": "user",
    "content": "What is the meaning of life?"
    }, {
      "role": "assistant",
      "content": "blank"
    }, {
      "role": "user",
      "content": "What might people describe as the meaning of life?"
    }],
  "model": "gpt-5-turbo-1"
}
```

Result

|                                      |     |
| ------------------------------------ | --- |
| `prompt_tokens`                      | 36  |
| `completion_tokens`                  | 213 |
| `x-ratelimit-remaining-tokens` delta | 16  |


### Request 3

Request:
```json
{
  "messages": [{
    "role": "user",
    "content": "When were the voyager space missions and what was their purpose?"
    }],
  "model": "gpt-5-turbo-1"
}
```

Result

|                                      |     |
| ------------------------------------ | --- |
| `prompt_tokens`                      | 21  |
| `completion_tokens`                  | 105 |
| `x-ratelimit-remaining-tokens` delta | 16  |


### Request 4


Request:
```json
{
  "messages": [{
        "role": "user",
        "content": "When were the voyager space missions and what was their purpose?"
    },
    {
        "content": "The Voyager space missions were launched in 1977. Their purpose was to study the outer planets of our solar system, including Jupiter, Saturn, Uranus, and Neptune, with the hope of gaining new insights into their composition, structure, and history. The spacecraft also carried a golden record containing sounds and images that were intended to serve as a message for any extraterrestrial life that might encounter it. The Voyager missions have been incredibly successful, providing scientists with a wealth of data and transforming our understanding of our solar system.",
        "role": "assistant"
      },
      {
          "role": "user",
        "content": "What things have they helped us to understand?"
      }],
  "model": "gpt-5-turbo-1"
}
```

Result

|                                      |     |
| ------------------------------------ | --- |
| `prompt_tokens`                      | 145 |
| `completion_tokens`                  | 180 |
| `x-ratelimit-remaining-tokens` delta | 16  |


### Request 5

Request:
```json
{
	"messages": [
		{
			"role": "user",
			"content": "Lorem ipsum dolor sit amet?"
		},
		{
			"role": "assistant",
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
		},
		{
			"role": "user",
			"content": "Ut enim ad minim veniam?"
		},
		{
			"role": "assistant",
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
		},
		{
			"role": "user",
			"content": "Lorem ipsum dolor sit amet?"
		},
		{
			"role": "assistant",
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
		},
		{
			"role": "user",
			"content": "Ut enim ad minim veniam?"
		},
		{
			"role": "assistant",
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
		},
		{
			"role": "user",
			"content": "Lorem ipsum dolor sit amet?"
		},
		{
			"role": "assistant",
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
		},
		{
			"role": "user",
			"content": "Ut enim ad minim veniam?"
		},
		{
			"role": "assistant",
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
		},
		{
			"role": "user",
			"content": "Lorem ipsum dolor sit amet?"
		},
		{
			"role": "assistant",
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
		},
		{
			"role": "user",
			"content": "Ut enim ad minim veniam?"
		},
		{
			"role": "assistant",
			"content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
		},
		{
			"role": "user",
			"content": "Duis aute irure dolor in reprehenderit?"
		}
	],
	"model": "gpt-5-turbo-1"
}
```

Result

|                                      |     |
| ------------------------------------ | --- |
| `prompt_tokens`                      | 914 |
| `completion_tokens`                  | 101 |
| `x-ratelimit-remaining-tokens` delta | 16  |


