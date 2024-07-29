# token limit tests - chat completions

## AOAI, non-streaming

Test setup:
- PAYG AOAI service.
- `gpt-4o` model
- TPM quota of `10,000` TPM
- no sleep time between requests

### max_tokens not set

Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false}
```

| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 9632                  | 368                  | n/a                           | 9352                        | n/a                                 | 9                             | n/a                                   | 355         | 14                    | 354                  |
| 200         | 9237                  | 395                  | 395                           | 8704                        | 648                                 | 8                             | 1                                     | 380         | 14                    | 381                  |
| 200         | 8836                  | 401                  | 401                           | 8056                        | 648                                 | 8                             | 0                                     | 388         | 14                    | 387                  |
| 200         | 8484                  | 352                  | 352                           | 7408                        | 648                                 | 8                             | 0                                     | 340         | 14                    | 338                  |
| 200         | 8197                  | 287                  | 287                           | 6760                        | 648                                 | 8                             | 0                                     | 279         | 14                    | 273                  |
| 200         | 7826                  | 371                  | 371                           | 6112                        | 648                                 | 8                             | 0                                     | 355         | 14                    | 357                  |
| 200         | 7449                  | 377                  | 377                           | 5464                        | 648                                 | 8                             | 0                                     | 366         | 14                    | 363                  |
| 200         | 7071                  | 378                  | 378                           | 4816                        | 648                                 | 8                             | 0                                     | 357         | 14                    | 364                  |
| 200         | 6492                  | 579                  | 579                           | 4168                        | 648                                 | 8                             | 0                                     | 562         | 14                    | 565                  |
| 200         | 6561                  | 313                  | -69                           | 4816                        | -648                                | 9                             | -1                                    | 299         | 14                    | 299                  |



Request timings:

```
2024-07-22 12:51:44.628740 Making request 0...
2024-07-22 12:51:48.667905 Making request 1...
2024-07-22 12:51:56.728022 Making request 2...
2024-07-22 12:52:05.394710 Making request 3...
2024-07-22 12:52:12.251899 Making request 4...
2024-07-22 12:52:17.282952 Making request 5...
2024-07-22 12:52:25.411888 Making request 6...
2024-07-22 12:52:33.711375 Making request 7...
2024-07-22 12:52:40.248547 Making request 8...
2024-07-22 12:52:52.531736 Making request 9...
```

NOTES:
- hit http read timeout and increased timeout from previous value of 10s



### max_tokens=1000

Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false, "max_tokens": 1000}
```


### max_tokens=2000

Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false, "max_tokens": 1000}
```


| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 9568                  | 432                  | n/a                           | 7992                        | n/a                                 | 9                             | n/a                                   | 412                        | 14                   | 418                      |
| 200         | 9107                  | 461                  | 461                           | 5984                        | 2008                                | 8                             | 1                                     | 441                        | 14                   | 447                      |
| 200         | 8768                  | 339                  | 339                           | 3976                        | 2008                                | 8                             | 0                                     | 323                        | 14                   | 325                      |
| 200         | 8436                  | 332                  | 332                           | 1968                        | 2008                                | 8                             | 0                                     | 319                        | 14                   | 318                      |
| 429         | 8422                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 8408                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 8394                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 8380                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 8366                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |
| 429         | 8352                  | 14                   | 14                            |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |


timings:
```
2024-07-22 12:46:02.576464 Making request 0...
2024-07-22 12:46:10.461020 Making request 1...
2024-07-22 12:46:17.657776 Making request 2...
2024-07-22 12:46:22.785817 Making request 3...
2024-07-22 12:46:27.339070 Making request 4...
2024-07-22 12:46:27.537631 Making request 5...
2024-07-22 12:46:27.702627 Making request 6...
2024-07-22 12:46:27.805224 Making request 7...
2024-07-22 12:46:27.920292 Making request 8...
2024-07-22 12:46:28.019330 Making request 9...
```

### max_tokens=2000 (extended)

- max_tokens=2000
- 100 requests
- 100 requests
- 1s sleep time




### max_tokens=10

- Added requests remaining header from AOAI response
- Increased number of requests sent to 20

Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false, "max_tokens": 10}
```


### max_tokens=10 (added 1s sleep)


Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false, "max_tokens": 10}
```
