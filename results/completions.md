# token limit tests - completions

## AOAI

Test setup:
- PAYG AOAI service.
- `gpt-3.5-turbo` model
- TPM quota of `10,000` TPM
- no sleep time between requests

### max_tokens not set

Request:
```json
{"prompt": "What is the meaning of life?"}
```

| Status code | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 9942                        | n/a                                 | 9                             | n/a                                   | 16                         | 7                    | 16                       |
| 200         | 9926                        | 16                                  | 8                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9910                        | 16                                  | 7                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9894                        | 16                                  | 6                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9878                        | 16                                  | 5                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9862                        | 16                                  | 4                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9846                        | 16                                  | 3                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9830                        | 16                                  | 2                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9814                        | 16                                  | 1                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9798                        | 16                                  | 0                             | 1                                     | 16                         | 7                    | 16                       |


### max_tokens not set, large response



Request:
```json
{"prompt": "What is the meaning of life?"}
```

| Status code | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 9942                        | n/a                                 | 9                             | n/a                                   | 16                         | 7                    | 16                       |
| 200         | 9926                        | 16                                  | 8                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9910                        | 16                                  | 7                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9894                        | 16                                  | 6                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9878                        | 16                                  | 5                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9862                        | 16                                  | 4                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9846                        | 16                                  | 3                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9830                        | 16                                  | 2                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9814                        | 16                                  | 1                             | 1                                     | 16                         | 7                    | 16                       |
| 200         | 9798                        | 16                                  | 0                             | 1                                     | 16                         | 7                    | 16                       |


### max_tokens=1000

Request:
```json
{"prompt": "What is the meaning of life?","max_tokens": 1000}
```

| Status code | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 9000                        | n/a                                 | 9                             | n/a                                   | 1000                       | 7                    | 1000                     |
| 200         | 8000                        | 1000                                | 9                             | 0                                     | 344                        | 7                    | 344                      |
| 200         | 7000                        | 1000                                | 8                             | 1                                     | 1000                       | 7                    | 1000                     |
| 200         | 6000                        | 1000                                | 9                             | -1                                    | 1000                       | 7                    | 1000                     |
| 200         | 5000                        | 1000                                | 9                             | 0                                     | 1001                       | 7                    | 1000                     |
| 200         | 4000                        | 1000                                | 9                             | 0                                     | 294                        | 7                    | 294                      |
| 200         | 3000                        | 1000                                | 8                             | 1                                     | 1000                       | 7                    | 1000                     |
| 200         | 4000                        | -1000                               | 9                             | -1                                    | 1000                       | 7                    | 1000                     |
| 200         | 5000                        | -1000                               | 9                             | 0                                     | 517                        | 7                    | 517                      |
| 200         | 4000                        | 1000                                | 8                             | 1                                     | 1000                       | 7                    | 1000                     |



Timings:

```
2024-07-25 11:03:35.937859 Making request 0...
2024-07-25 11:03:45.747654 Making request 1...
2024-07-25 11:03:51.111328 Making request 2...
2024-07-25 11:04:04.675520 Making request 3...
2024-07-25 11:04:17.994829 Making request 4...
2024-07-25 11:04:32.113537 Making request 5...
2024-07-25 11:04:35.702062 Making request 6...
2024-07-25 11:04:51.660359 Making request 7...
2024-07-25 11:05:04.739093 Making request 8...
2024-07-25 11:05:11.327506 Making request 9...
```



### max_tokens=2000

Request:
```json
{"prompt": "What is the meaning of life?","max_tokens": 2000}
```



| Status code | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 8000                        | n/a                                 | 9                             | n/a                                   | 218                        | 7                    | 218                      |
| 200         | 6000                        | 2000                                | 8                             | 1                                     | 0                          | 7                    | 2000                     |
| 200         | 4000                        | 2000                                | 9                             | -1                                    | 1094                       | 7                    | 1095                     |
| 200         | 2000                        | 2000                                | 9                             | 0                                     | 312                        | 7                    | 312                      |
| 200         | 0                           | 2000                                | 8                             | 1                                     | 661                        | 7                    | 671                      |
| 200         | 0                           | n/a                                 | 9                             | -1                                    | 379                        | 7                    | 379                      |
| 200         | 0                           | n/a                                 | 8                             | 1                                     | 2000                       | 7                    | 2000                     |
| 200         | 0                           | n/a                                 | 9                             | -1                                    | 2000                       | 7                    | 2000                     |
| 200         | 2000                        | n/a                                 | 9                             | 0                                     | 947                        | 7                    | 948                      |
| 200         | 4000                        | -2000                               | 9                             | 0                                     | 2000                       | 7                    | 2000                     |


Timings:

```
2024-07-25 11:06:22.129041 Making request 0...
2024-07-25 11:06:24.915218 Making request 1...
2024-07-25 11:06:51.965077 Making request 2...
2024-07-25 11:07:09.328920 Making request 3...
2024-07-25 11:07:12.304256 Making request 4...
2024-07-25 11:07:22.981447 Making request 5...
2024-07-25 11:07:28.664656 Making request 6...
2024-07-25 11:07:53.536844 Making request 7...
2024-07-25 11:08:17.117373 Making request 8...
2024-07-25 11:08:28.817586 Making request 9...
```