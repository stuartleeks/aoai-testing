# token limit tests - chat completions

## AOAI, non-streaming

Test setup:
- PAYG AOAI service.
- `gpt-4` model
- TPM quota of `10,000` TPM
- no sleep time between requests
- using the chat_non_streaming_direct.py script as the focus is not on the APIM counting at this point

### max_tokens not set

Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false}
```
| Status code | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) | Payload length |
| ----------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ | -------------- |
| 200         | 8056                        | n/a                                 | 9                             | n/a                                   | 100                        | 14                   | 100                      | 90             |
| 200         | 7408                        | 648                                 | 8                             | 1                                     | 98                         | 14                   | 98                       | 90             |
| 200         | 6760                        | 648                                 | 7                             | 1                                     | 110                        | 14                   | 110                      | 90             |
| 200         | 6112                        | 648                                 | 6                             | 1                                     | 96                         | 14                   | 96                       | 90             |
| 200         | 5464                        | 648                                 | 5                             | 1                                     | 77                         | 14                   | 77                       | 90             |
| 200         | 4816                        | 648                                 | 4                             | 1                                     | 99                         | 14                   | 99                       | 90             |
| 200         | 4168                        | 648                                 | 4                             | 0                                     | 100                        | 14                   | 100                      | 90             |
| 200         | 3520                        | 648                                 | 4                             | 0                                     | 86                         | 14                   | 86                       | 90             |
| 200         | 2872                        | 648                                 | 4                             | 0                                     | 104                        | 14                   | 104                      | 90             |
| 200         | 2224                        | 648                                 | 4                             | 0                                     | 82                         | 14                   | 82                       | 90             |



Request timings:

```
2024-08-07 07:31:54.142147 Making request 0...
2024-08-07 07:31:56.211949 Making request 1...
2024-08-07 07:31:58.130112 Making request 2...
2024-08-07 07:32:00.342309 Making request 3...
2024-08-07 07:32:02.322396 Making request 4...
2024-08-07 07:32:04.009399 Making request 5...
2024-08-07 07:32:06.001053 Making request 6...
2024-08-07 07:32:08.005497 Making request 7...
2024-08-07 07:32:09.747986 Making request 8...
2024-08-07 07:32:11.831739 Making request 9...
```



### max_tokens not set - 2

Request:
```json
{"messages": [{"role": "user","content": "Imagine you are a school teacher and you have a room full of eight year old children. Your task is to get them excited and interested in science and today\'s topic is gravity. How would you explain gravity to captivate their interest?"}],"stream": false}
```

| Status code | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) | Payload length |
| ----------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ | -------------- |
| 200         | 9301                        | n/a                                 | 9                             | n/a                                   | 328                        | 54                   | 328                      | 295            |
| 200         | 8602                        | 699                                 | 8                             | 1                                     | 324                        | 54                   | 324                      | 295            |
| 200         | 7903                        | 699                                 | 8                             | 0                                     | 282                        | 54                   | 282                      | 295            |
| 200         | 7204                        | 699                                 | 8                             | 0                                     | 310                        | 54                   | 310                      | 295            |
| 200         | 6505                        | 699                                 | 8                             | 0                                     | 331                        | 54                   | 331                      | 295            |
| 200         | 5806                        | 699                                 | 8                             | 0                                     | 264                        | 54                   | 264                      | 295            |
| 200         | 5107                        | 699                                 | 8                             | 0                                     | 286                        | 54                   | 286                      | 295            |
| 200         | 4408                        | 699                                 | 8                             | 0                                     | 321                        | 54                   | 321                      | 295            |
| 200         | 3709                        | 699                                 | 8                             | 0                                     | 293                        | 54                   | 293                      | 295            |
| 200         | 3010                        | 699                                 | 8                             | 0                                     | 271                        | 54                   | 271                      | 295            |

Request timings:

```
2024-08-07 07:43:23.258355 Making request 0...
2024-08-07 07:43:29.265228 Making request 1...
2024-08-07 07:43:35.184430 Making request 2...
2024-08-07 07:43:40.380999 Making request 3...
2024-08-07 07:43:46.024500 Making request 4...
2024-08-07 07:43:52.143542 Making request 5...
2024-08-07 07:43:57.076619 Making request 6...
2024-08-07 07:44:02.477543 Making request 7...
2024-08-07 07:44:08.797529 Making request 8...
2024-08-07 07:44:14.550720 Making request 9...
```


### max_tokens not set - 3

Request:
```json
{"messages": [ {"role": "system","content": [{"type": "text","text": "You are an AI assistant that helps people find information."}]},{"role": "user","content": [{"type": "text","text": "What is gravity?"}]},{"role": "assistant","content": [{"type": "text","text": "Gravity is a fundamental force of nature that attracts two bodies towards each other. It is the force that causes objects to fall to the ground when dropped, and it keeps the planets in orbit around the Sun. The force of gravity is proportional to the mass of the objects and inversely proportional to the square of the distance between their centers. This concept was described by Isaac Newton in the 17th century with his law of universal gravitation. Later, Albert Einstein\'s theory of general relativity, proposed in the early 20th century, provided a deeper understanding by describing gravity not as a force, but as a curvature of spacetime caused by mass and energy."}]},{"role": "user","content": [{"type": "text","text": "Imagine you are a school teacher and you have a room full of eight year old children. Your task is to get them excited and interested in science and today\'s topic is gravity. How would you explain gravity to captivate their interest?"}]}],"stream": false}
```

| Status code | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) | Payload length |
| ----------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ | -------------- |
| 200         | 9112                        | n/a                                 | 9                             | n/a                                   | 392                        | 214                  | 392                      | 1252           |
| 200         | 8224                        | 888                                 | 8                             | 1                                     | 292                        | 214                  | 292                      | 1252           |
| 200         | 7336                        | 888                                 | 8                             | 0                                     | 343                        | 214                  | 343                      | 1252           |
| 200         | 6448                        | 888                                 | 8                             | 0                                     | 375                        | 214                  | 375                      | 1252           |
| 200         | 5560                        | 888                                 | 8                             | 0                                     | 308                        | 214                  | 308                      | 1252           |
Request timings:

```
2024-08-07 07:49:50.107626 Making request 0...
2024-08-07 07:49:57.184593 Making request 1...
2024-08-07 07:50:02.496695 Making request 2...
2024-08-07 07:50:08.689740 Making request 3...
2024-08-07 07:50:15.449552 Making request 4...
```


### max_tokens not set - 4


| Status code | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) | Payload length |
| ----------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ | -------------- |
| 200         | 8881                        | n/a                                 | 9                             | n/a                                   | 471                        | 280                  | 471                      | 2127           |
| 200         | 7762                        | 1119                                | 8                             | 1                                     | 464                        | 280                  | 464                      | 2127           |


### max_tokens not set - summary

| Rate limit tokens remaining delta | prompt tokens | payload length |
| --------------------------------- | ------------- | -------------- |
| 648                               | 14            | 90             |
| 699                               | 54            | 295            |
| 888                               | 214           | 1252           |
| 1119                              | 280           | 2127           |

### max_tokens=1000

Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false, "max_tokens": 1000}
```

| Status code | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 8992                        | n/a                                 | 9                             | n/a                                   | 108                        | 14                   | 108                      |
| 200         | 7984                        | 1008                                | 8                             | 1                                     | 84                         | 14                   | 84                       |
| 200         | 6976                        | 1008                                | 7                             | 1                                     | 94                         | 14                   | 94                       |
| 200         | 5968                        | 1008                                | 6                             | 1                                     | 75                         | 14                   | 75                       |
| 200         | 4960                        | 1008                                | 5                             | 1                                     | 82                         | 14                   | 82                       |
| 200         | 3952                        | 1008                                | 4                             | 1                                     | 101                        | 14                   | 101                      |
| 200         | 2944                        | 1008                                | 4                             | 0                                     | 100                        | 14                   | 100                      |
| 200         | 1936                        | 1008                                | 4                             | 0                                     | 95                         | 14                   | 95                       |
| 200         | 928                         | 1008                                | 4                             | 0                                     | 96                         | 14                   | 96                       |
| 429         |                             | n/a                                 |                               | n/a                                   | 0                          |                      |                          |



Request timings:

```
2024-08-07 07:34:45.170519 Making request 0...
2024-08-07 07:34:47.740399 Making request 1...
2024-08-07 07:34:49.512147 Making request 2...
2024-08-07 07:34:51.440501 Making request 3...
2024-08-07 07:34:53.046253 Making request 4...
2024-08-07 07:34:54.794715 Making request 5...
2024-08-07 07:34:56.832862 Making request 6...
2024-08-07 07:34:58.881123 Making request 7...
2024-08-07 07:35:00.822346 Making request 8...
2024-08-07 07:35:02.741131 Making request 9...
```


### max_tokens=2000

Request:
```json
{"messages": [{"role": "user","content": "What is the meaning of life?"}],"stream": false, "max_tokens": 2000}
```

| Status code | Rate limit tokens remaining | Rate limit tokens remaining (delta) | Rate limit requests remaining | Rate limit requests remaining (delta) | Tiktoken count (generated) | Body tokens (prompt) | Body tokens (completion) |
| ----------- | --------------------------- | ----------------------------------- | ----------------------------- | ------------------------------------- | -------------------------- | -------------------- | ------------------------ |
| 200         | 7992                        | n/a                                 | 9                             | n/a                                   | 84                         | 14                   | 84                       |
| 200         | 5984                        | 2008                                | 8                             | 1                                     | 113                        | 14                   | 113                      |
| 200         | 3976                        | 2008                                | 7                             | 1                                     | 77                         | 14                   | 77                       |
| 200         | 1968                        | 2008                                | 6                             | 1                                     | 86                         | 14                   | 86                       |


Request timings:
```
2024-08-07 07:36:16.481233 Making request 0...
2024-08-07 07:36:18.340450 Making request 1...
2024-08-07 07:36:20.770149 Making request 2...
2024-08-07 07:36:22.480909 Making request 3...
```
