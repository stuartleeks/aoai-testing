# token limit test: embeddings

- [token limit test: embeddings](#token-limit-test-embeddings)
	- [AOAI, short embedding text](#aoai-short-embedding-text)
		- [Test 1: no sleep](#test-1-no-sleep)
		- [Test 2: 1s sleep](#test-2-1s-sleep)
		- [Test 3: 10s sleep](#test-3-10s-sleep)


## AOAI, short embedding text

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

### Test 3: 10s sleep

Embedding text: `This is some text to generate embeddings for`

Results:

| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Body tokens (prompt) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | -------------------- |
| 200         | 9984                  | 8                    | n/a                           | 989                         | n/a                                 | 8                    |
| 200         | 9968                  | 8                    | 16                            | 978                         | 11                                  | 8                    |
| 200         | 9952                  | 8                    | 16                            | 967                         | 11                                  | 8                    |
| 200         | 9936                  | 8                    | 16                            | 956                         | 11                                  | 8                    |
| 200         | 9920                  | 8                    | 16                            | 945                         | 11                                  | 8                    |
| 200         | 9904                  | 8                    | 16                            | 934                         | 11                                  | 8                    |
| 200         | 9904                  | 8                    | 0                             | 934                         | 0                                   | 8                    |
| 200         | 9904                  | 8                    | 0                             | 934                         | 0                                   | 8                    |
| 200         | 9904                  | 8                    | 0                             | 934                         | 0                                   | 8                    |
| 200         | 9904                  | 8                    | 0                             | 934                         | 0                                   | 8                    |


Notes:
* All requests are successful with the 10s sleep
* The APIM tokens consumed matches the expected 8 tokens per request based on the body content
  * But the APIM remaining tokens is decremented by 16 tokens per request (this is different from the previous tests)
* The rate limit tokens remaining is decremented by 11 tokens per request
  * This suggests that the rate limit is being decremented by 11 tokens per request, which is higher than the 8 tokens per request that the body content suggests
  * This applies for the first 6 requests (i.e. the first minute). It then stops decrementing the rate limit tokens remaining which is consistent with a 1 minute sliding window
