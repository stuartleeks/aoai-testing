# token counting tests - chat completions

## AOAI

Test setup:
- PAYG AOAI service.
- `gpt-3.5-turbo` model
- TPM quota of `10,000` TPM


### Non-streaming (baseline)


Payload:

```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false,"max_tokens": 100}
```

2 requests:

| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 9699                  | 71                   | n/a                           | 9700                        | n/a                                 | 7                             | n/a                                   | 56                         | 15                   | 56                       |
| 200         | 9591                  | 108                  | 108                           | 9600                        | 100                                 | 6                             | 1                                     | 93                         | 15                   | 93                       |


NOTES:
- tiktoken count (i.e. the token count from the test app using tiktoken) matches the completion tokens from the body
- APIM tokens consumed (from the APIM policy) matches the total tokens from the body

### Streaming

Payload:

```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": true,"max_tokens": 100}
```


| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Tiktoken count (generated) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | ----------------------------- | -------------------------- |
| 200         | 9986                  | 14                   | n/a                           | 9900                        | n/a                                 | 9                             | 92                         |
| 200         | 9881                  | 14                   | 105                           | 9800                        | 100                                 | 8                             | 100                        |
| 200         | 9769                  | 14                   | 112                           | 9700                        | 100                                 | 7                             | 88                         |
| 200         | 9668                  | 14                   | 101                           | 9600                        | 100                                 | 6                             | 72                         |
| 200         | 9583                  | 14                   | 85                            | 9500                        | 100                                 | 5                             | 90                         |
| 200         | 9481                  | 14                   | 102                           | 9400                        | 100                                 | 4                             | 90                         |
| 200         | 9378                  | 14                   | 103                           | 9300                        | 100                                 | 3                             | 100                        |
| 200         | 9266                  | 14                   | 112                           | 9200                        | 100                                 | 2                             | 76                         |
| 200         | 9177                  | 14                   | 89                            | 9100                        | 100                                 | 1                             | 97                         |
| 200         | 9067                  | 14                   | 110                           | 9000                        | 100                                 | 1                             | 99                         |


NOTES:
- APIM tokens consumed (from the APIM policy) matches neither the previous prompt tokens or the tiktoken count

