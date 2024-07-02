# token limit test: embeddings


## AOAI

Test setup:
- PAYG AOAI service.
- `text-embedding-ada-002` model
- TPM quota of `1,000` TPM

### Test 1: no sleep

Embedding text: `This is some text to generate embeddings for`

Results:

| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Body tokens (prompt) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | -------------------- |
| 200         | 9984                  | 8                    | n/a                           | 989                         | n/a                                 | 8                    |
| 429         | 9976                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9968                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9960                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9952                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9944                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9936                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9928                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9920                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9912                  | 8                    | 8                             |                             | n/a                                 |                      |

Notes:
* This test was run after an idle period
  * The payload in the body shows of the first request shows usage of 8 tokens
* Only the first request was successful
  * The rate limit tokens remaining is 989 which suggests that 11 tokens have been decremented from the 1000 TPM limit
  * With a 1000 TPM quota, that should allow ~167 tokens in 10 seconds. Even if the requests took 11 tokens each, that would make 110 tokens for the 10 requests

### Test 2: 1s sleep

Embedding text: `This is some text to generate embeddings for`


Results:


| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Body tokens (prompt) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | -------------------- |
| 200         | 9984                  | 8                    | n/a                           | 989                         | n/a                                 | 8                    |
| 429         | 9976                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9968                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9960                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9952                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9944                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9936                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9928                  | 8                    | 8                             |                             | n/a                                 |                      |
| 429         | 9920                  | 8                    | 8                             |                             | n/a                                 |                      |
| 200         | 9904                  | 8                    | 16                            | 978                         | n/a                                 | 8                    |


Notes:
* Even with a 1s sleep between requests, only the first and last requests were allowed through
* The APIM tokens consumed matches the expected 8 tokens per request based on the body content (even though it's not clear what the AOAI remaining tokens is based on)

