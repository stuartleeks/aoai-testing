# token limit test: embeddings

- [token limit test: embeddings](#token-limit-test-embeddings)
	- [AOAI, short embedding text, 1000TPM quota,](#aoai-short-embedding-text-1000tpm-quota)
		- [Test 1: 1000TPM quota, short text, no sleep](#test-1-1000tpm-quota-short-text-no-sleep)
		- [Test 2: 1000TPM quota, short text, 1s sleep](#test-2-1000tpm-quota-short-text-1s-sleep)
		- [Test 3: 1000TPM quota, short text, 10s sleep](#test-3-1000tpm-quota-short-text-10s-sleep)
	- [AOAI, short embedding text, 10,000TPM quota](#aoai-short-embedding-text-10000tpm-quota)
	- [AOAI, 46-token embedding text, 10,000TPM quota](#aoai-46-token-embedding-text-10000tpm-quota)
	- [AOAI, Comparison of body vs header token amounts](#aoai-comparison-of-body-vs-header-token-amounts)


## AOAI, short embedding text, 1000TPM quota, 

Test setup:
- PAYG AOAI service.
- `text-embedding-ada-002` model
- TPM quota of `1,000` TPM

Embedding text: `This is some text to generate embeddings for`

**UPDATE: I just realised that 1000 TPM corresponds to 6RPM!! So the rate-limiting that is kicking in is based on number of requests not the number of tokens!**


### Test 1: 1000TPM quota, short text, no sleep

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

### Test 2: 1000TPM quota, short text, 1s sleep

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

### Test 3: 1000TPM quota, short text, 10s sleep

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

<!-- 
## AOAI, long embedding text, 1000TPM quota

Test setup:
- PAYG AOAI service.
- `text-embedding-ada-002` model
- TPM quota of `1,000` TPM


Embedding text: `This is some text to generate embeddings for and islonger than the previous text which really was quite short. This would be a good place to put a short story about a dog. I mean, who doesn''t like stories about dogs?`

### Test 1: 1000TPM quota, longer text, no sleep

Results:

| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Body tokens (prompt) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | -------------------- |
| 200         | 9904                  | 48                   | n/a                           | 946                         | n/a                                 | 48                   |
| 429         | 9856                  | 48                   | 48                            |                             | n/a                                 |                      |
| 429         | 9808                  | 48                   | 48                            |                             | n/a                                 |                      |
| 429         | 9760                  | 48                   | 48                            |                             | n/a                                 |                      |
| 429         | 9712                  | 48                   | 48                            |                             | n/a                                 |                      |
| 429         | 9664                  | 48                   | 48                            |                             | n/a                                 |                      |
| 429         | 9616                  | 48                   | 48                            |                             | n/a                                 |                      |
| 429         | 9568                  | 48                   | 48                            |                             | n/a                                 |                      |
| 429         | 9520                  | 48                   | 48                            |                             | n/a                                 |                      |
| 429         | 9472                  | 48                   | 48                            |                             | n/a                                 |                      |


Notes:
* Again, the APIM tokens consumed matches the body tokens
  * And again, neither matches the decrement in the APIM tokens remaining (54 tokens this time) -->


## AOAI, short embedding text, 10,000TPM quota

Test setup:
- PAYG AOAI service.
- `text-embedding-ada-002` model
- TPM quota of `10,000` TPM
- Embedding text: `This is some text to generate embeddings for`



## AOAI, 46-token embedding text, 10,000TPM quota

Test setup:
- PAYG AOAI service.
- `text-embedding-ada-002` model
- TPM quota of `10,000` TPM
Embedding text: `This is some text to generate embeddings for and is longer than the previous text which really was quite short. This would be a good place to put a short story about a dog. I mean, who doesn''t like stories about dogs?`


| Status code | APIM tokens remaining | APIM tokens consumed | APIM tokens remaining (delta) | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Body tokens (prompt) |
| ----------- | --------------------- | -------------------- | ----------------------------- | --------------------------- | ----------------------------------- | -------------------- |
| 200         | 9908                  | 46                   | n/a                           | 9946                        | n/a                                 | 46                   |
| 200         | 9816                  | 46                   | 92                            | 9892                        | 54                                  | 46                   |
| 200         | 9724                  | 46                   | 92                            | 9838                        | 54                                  | 46                   |
| 200         | 9632                  | 46                   | 92                            | 9784                        | 54                                  | 46                   |
| 200         | 9540                  | 46                   | 92                            | 9730                        | 54                                  | 46                   |
| 200         | 9448                  | 46                   | 92                            | 9676                        | 54                                  | 46                   |
| 200         | 9356                  | 46                   | 92                            | 9622                        | 54                                  | 46                   |
| 200         | 9264                  | 46                   | 92                            | 9568                        | 54                                  | 46                   |
| 200         | 9172                  | 46                   | 92                            | 9514                        | 54                                  | 46                   |
| 200         | 9080                  | 46                   | 92                            | 9460                        | 54                                  | 46                   |



## AOAI, Comparison of body vs header token amounts

Test setup:
- PAYG AOAI service.
- `text-embedding-ada-002` model

For this test I sent different embedding texts to capture the `usage.prompt_tokens` value from the request body and the difference in the `x-ratelimit-remaining-tokens` header values between requests.

| `usage.prompt_tokens` | `x-ratelimit-remaining-tokens` delta | Diff as % of `usage.prompt_tokens` |
| --------------------- | ------------------------------------ | ---------------------------------- |
| 8                     | 11                                   | 38%                                |
| 46                    | 54                                   | 17%                                |
| 1751                  | 1897                                 | 8%                                 |
