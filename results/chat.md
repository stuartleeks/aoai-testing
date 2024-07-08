# token limit tests - chat completions

## AOAI, non-streaming

Test setup:
- PAYG AOAI service.
- `gpt-3.5-turbo` model
- TPM quota of `10,000` TPM
- no sleep time between requests

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




### max_tokens=10

- Added requests remaining header from AOAI response
- Increased number of requests sent to 20

Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false, "max_tokens": 10}
```

| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 9975                  | 25                   | n/a                           | 9990                        | n/a                                 | 9                             | n/a                                   | 10                         | 15                   | 10                       |
| 200         | 9950                  | 25                   | 25                            | 9980                        | 10                                  | 8                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9925                  | 25                   | 25                            | 9970                        | 10                                  | 7                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9900                  | 25                   | 25                            | 9960                        | 10                                  | 6                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9875                  | 25                   | 25                            | 9950                        | 10                                  | 5                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9850                  | 25                   | 25                            | 9940                        | 10                                  | 4                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9825                  | 25                   | 25                            | 9930                        | 10                                  | 3                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9800                  | 25                   | 25                            | 9920                        | 10                                  | 2                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9775                  | 25                   | 25                            | 9910                        | 10                                  | 1                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9750                  | 25                   | 25                            | 9900                        | 10                                  | 0                             | 1                                     | 10                         | 15                   | 10                       |
| 429         | 9736                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 9722                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 9708                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 9694                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 9680                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 9666                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 9652                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 9638                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 9624                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 9610                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |





### max_tokens=10 (added 1s sleep)


Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false, "max_tokens": 10}
```


| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 9975                  | 25                   | n/a                           | 9990                        | n/a                                 | 9                             | n/a                                   | 10                         | 15                   | 10                       |
| 200         | 9950                  | 25                   | 25                            | 9980                        | 10                                  | 8                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9925                  | 25                   | 25                            | 9970                        | 10                                  | 7                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9900                  | 25                   | 25                            | 9960                        | 10                                  | 6                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9875                  | 25                   | 25                            | 9950                        | 10                                  | 5                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9850                  | 25                   | 25                            | 9940                        | 10                                  | 4                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9825                  | 25                   | 25                            | 9930                        | 10                                  | 3                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9800                  | 25                   | 25                            | 9920                        | 10                                  | 2                             | 1                                     | 10                         | 15                   | 10                       |
| 200         | 9775                  | 25                   | 25                            | 9910                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |
| 200         | 9750                  | 25                   | 25                            | 9900                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |
| 200         | 9725                  | 25                   | 25                            | 9890                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |
| 200         | 9700                  | 25                   | 25                            | 9880                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |
| 200         | 9675                  | 25                   | 25                            | 9870                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |
| 200         | 9650                  | 25                   | 25                            | 9860                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |
| 200         | 9625                  | 25                   | 25                            | 9850                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |
| 200         | 9600                  | 25                   | 25                            | 9840                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |
| 200         | 9575                  | 25                   | 25                            | 9830                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |
| 200         | 9550                  | 25                   | 25                            | 9820                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |
| 200         | 9525                  | 25                   | 25                            | 9810                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |
| 200         | 9500                  | 25                   | 25                            | 9800                        | 10                                  | 2                             | 0                                     | 10                         | 15                   | 10                       |