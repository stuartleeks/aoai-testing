# token limit tests - chat completions

## AOAI, non-streaming

Test setup:
- PAYG AOAI service.
- `gpt-3.5-turbo` model
- TPM quota of `10,000` TPM

### max_tokens not set

Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false}
```

 | Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
 | ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | -------------------------- | -------------------- | ------------------------ |
 | 200         | 9852                  | 148                  | n/a                           | 9984                        | n/a                                 | 133                        | 15                   | 133                      |
 | 200         | 9752                  | 100                  | 100                           | 9968                        | 16                                  | 85                         | 15                   | 85                       |
 | 200         | 9662                  | 90                   | 90                            | 9952                        | 16                                  | 75                         | 15                   | 75                       |
 | 200         | 9456                  | 206                  | 206                           | 9936                        | 16                                  | 191                        | 15                   | 191                      |
 | 200         | 9385                  | 71                   | 71                            | 9920                        | 16                                  | 56                         | 15                   | 56                       |
 | 200         | 9249                  | 136                  | 136                           | 9904                        | 16                                  | 121                        | 15                   | 121                      |
 | 200         | 9152                  | 97                   | 97                            | 9888                        | 16                                  | 82                         | 15                   | 82                       |
 | 200         | 9075                  | 77                   | 77                            | 9872                        | 16                                  | 62                         | 15                   | 62                       |
 | 200         | 8935                  | 140                  | 140                           | 9856                        | 16                                  | 125                        | 15                   | 125                      |
 | 200         | 8822                  | 113                  | 113                           | 9840                        | 16                                  | 98                         | 15                   | 98                       |


### max_tokens=1000

Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false, "max_tokens": 1000}
```

| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 9879                  | 121                  | n/a                           | 9000                        | n/a                                 | 106                        | 15                   | 106                      |
| 200         | 9783                  | 96                   | 96                            | 8000                        | 1000                                | 81                         | 15                   | 81                       |
| 200         | 9687                  | 96                   | 96                            | 7000                        | 1000                                | 81                         | 15                   | 81                       |
| 200         | 9551                  | 136                  | 136                           | 6000                        | 1000                                | 121                        | 15                   | 121                      |
| 200         | 9407                  | 144                  | 144                           | 5000                        | 1000                                | 129                        | 15                   | 129                      |
| 200         | 9259                  | 148                  | 148                           | 4000                        | 1000                                | 133                        | 15                   | 133                      |
| 200         | 9136                  | 123                  | 123                           | 3000                        | 1000                                | 108                        | 15                   | 108                      |
| 200         | 9008                  | 128                  | 128                           | 2000                        | 1000                                | 113                        | 15                   | 113                      |
| 200         | 8915                  | 93                   | 93                            | 1000                        | 1000                                | 78                         | 15                   | 78                       |
| 200         | 8801                  | 114                  | 114                           | 0                           | 1000                                | 99                         | 15                   | 99                       |


### max_tokens=2000

Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false, "max_tokens": 1000}
```

| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 9886                  | 114                  | n/a                           | 8000                        | n/a                                 | 99                         | 15                   | 99                       |
| 200         | 9819                  | 67                   | 67                            | 6000                        | 2000                                | 52                         | 15                   | 52                       |
| 200         | 9694                  | 125                  | 125                           | 4000                        | 2000                                | 110                        | 15                   | 110                      |
| 200         | 9615                  | 79                   | 79                            | 2000                        | 2000                                | 64                         | 15                   | 64                       |
| 200         | 9503                  | 112                  | 112                           | 0                           | 2000                                | 97                         | 15                   | 97                       |
| 429         | 9489                  | 14                   | 14                            |                             | n/a                                 | 0                          |                      |                          |
| 429         | 9475                  | 14                   | 14                            |                             | n/a                                 | 0                          |                      |                          |
| 429         | 9461                  | 14                   | 14                            |                             | n/a                                 | 0                          |                      |                          |
| 429         | 9447                  | 14                   | 14                            |                             | n/a                                 | 0                          |                      |                          |
| 429         | 9433                  | 14                   | 14                            |                             | n/a                                 | 0                          |                      |                          |




