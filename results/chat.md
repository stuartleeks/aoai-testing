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

| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 9911                  | 89                   | n/a                           | 9000                        | n/a                                 | 9                             | n/a                                   | 74                         | 15                   | 74                       |
| 200         | 9797                  | 114                  | 114                           | 8000                        | 1000                                | 8                             | 1                                     | 99                         | 15                   | 99                       |
| 200         | 9705                  | 92                   | 92                            | 7000                        | 1000                                | 7                             | 1                                     | 77                         | 15                   | 77                       |
| 200         | 9554                  | 151                  | 151                           | 6000                        | 1000                                | 6                             | 1                                     | 136                        | 15                   | 136                      |
| 200         | 9430                  | 124                  | 124                           | 5000                        | 1000                                | 5                             | 1                                     | 109                        | 15                   | 109                      |
| 200         | 9286                  | 144                  | 144                           | 4000                        | 1000                                | 4                             | 1                                     | 129                        | 15                   | 129                      |
| 200         | 9179                  | 107                  | 107                           | 3000                        | 1000                                | 3                             | 1                                     | 92                         | 15                   | 92                       |
| 200         | 9086                  | 93                   | 93                            | 2000                        | 1000                                | 2                             | 1                                     | 78                         | 15                   | 78                       |
| 200         | 8984                  | 102                  | 102                           | 1000                        | 1000                                | 1                             | 1                                     | 87                         | 15                   | 87                       |
| 200         | 8876                  | 108                  | 108                           | 0                           | 1000                                | 1                             | 0                                     | 93                         | 15                   | 93                       |

NOTE: below are the timestamps captured for sending these requests:

```
2024-07-08 15:34:34.374693 Making request 0...
2024-07-08 15:34:35.286722 Making request 1...
2024-07-08 15:34:36.567960 Making request 2...
2024-07-08 15:34:37.611665 Making request 3...
2024-07-08 15:34:39.026420 Making request 4...
2024-07-08 15:34:40.315840 Making request 5...
2024-07-08 15:34:41.867458 Making request 6...
2024-07-08 15:34:42.858961 Making request 7...
2024-07-08 15:34:43.902197 Making request 8...
2024-07-08 15:34:45.016835 Making request 9...
```

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


NOTE: below are the timestamps captured for sending these requests:

```
2024-07-08 14:13:30.030451 Making request 0...
2024-07-08 14:13:30.345956 Making request 1...
2024-07-08 14:13:30.703761 Making request 2...
2024-07-08 14:13:31.010155 Making request 3...
2024-07-08 14:13:31.329538 Making request 4...
2024-07-08 14:13:31.646356 Making request 5...
2024-07-08 14:13:31.912617 Making request 6...
2024-07-08 14:13:32.231183 Making request 7...
2024-07-08 14:13:32.536956 Making request 8...
2024-07-08 14:13:32.829056 Making request 9...
2024-07-08 14:13:33.189924 Making request 10...
2024-07-08 14:13:33.307263 Making request 11...
2024-07-08 14:13:33.418216 Making request 12...
2024-07-08 14:13:33.524874 Making request 13...
2024-07-08 14:13:33.651796 Making request 14...
2024-07-08 14:13:33.750431 Making request 15...
2024-07-08 14:13:33.852223 Making request 16...
2024-07-08 14:13:33.974065 Making request 17...
2024-07-08 14:13:34.079579 Making request 18...
2024-07-08 14:13:34.181464 Making request 19...
```


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

NOTE: below are the timestamps captured for sending these requests:

```
2024-07-08 15:00:00.758317 Making request 0...
2024-07-08 15:00:02.119477 Making request 1...
2024-07-08 15:00:03.674367 Making request 2...
2024-07-08 15:00:04.998926 Making request 3...
2024-07-08 15:00:06.287145 Making request 4...
2024-07-08 15:00:07.529691 Making request 5...
2024-07-08 15:00:08.838585 Making request 6...
2024-07-08 15:00:10.225659 Making request 7...
2024-07-08 15:00:11.543337 Making request 8...
2024-07-08 15:00:12.876239 Making request 9...
2024-07-08 15:00:14.168985 Making request 10...
2024-07-08 15:00:15.462093 Making request 11...
2024-07-08 15:00:16.754209 Making request 12...
2024-07-08 15:00:18.016338 Making request 13...
2024-07-08 15:00:19.301173 Making request 14...
2024-07-08 15:00:20.667600 Making request 15...
2024-07-08 15:00:21.981375 Making request 16...
2024-07-08 15:00:23.321452 Making request 17...
2024-07-08 15:00:24.600305 Making request 18...
2024-07-08 15:00:25.933166 Making request 19...
```