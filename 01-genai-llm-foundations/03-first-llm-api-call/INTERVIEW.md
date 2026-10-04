# Interview pack: your first LLM API call, done properly

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb), run against **Claude Haiku 4.5** with the
`anthropic` Python SDK 1.11. In §5 the 429/529 errors were **injected on purpose** (they can't be triggered on demand);
the retrying was the SDK's own. Everything else is a real API response.

---

### 1. Your call returned 200 OK, but the answer stops mid-sentence. What happened? · Junior
- **Trap:** "The model glitched. Retry it."
- **Answer:** It hit `max_tokens`. The response is a normal **200 OK** with `stop_reason: "max_tokens"`, and **no exception is raised**. With `max_tokens=25`, the answer stopped at *"1. **Invalid authentication** - Missing or expired credentials/"*. Always check `stop_reason` before trusting `content`.
- **Follow-up:** It happens on 2% of production calls. What do you do?
- **Follow-up answer:** Log `stop_reason` and `usage.output_tokens` on every call, and alert on `max_tokens`. Then either raise `max_tokens` for that route or ask for shorter output in the prompt. Don't retry blindly: the same request will hit the same limit.
- Notebook: [§2](notebook.ipynb#2-read-the-whole-response)

### 2. Does streaming make the model faster? · Junior
- **Trap:** "Yes. Streaming is a performance optimisation."
- **Answer:** No. The total time was the same: **3.05 s streaming vs 3.03 s not** (median of 5, ~258 output tokens). What changes is when the user sees the first words: **0.60 s vs 3.03 s**, about 5× sooner.
- **Follow-up:** Your backend calls the LLM, then post-processes the full JSON before replying. Should it stream?
- **Follow-up answer:** Streaming barely helps a pipeline that needs the complete answer, because total time is unchanged. It still helps keep long calls alive under a tight timeout (see Q5). Stream when a person is watching, or when an answer might take long.
- Notebook: [§3](notebook.ipynb#3-streaming-same-answer-sooner)

### 3. Which errors should you retry? · Mid
- **Trap:** "Wrap the call in a retry loop and retry everything."
- **Answer:** Only the temporary ones: rate limits (429), server errors and overload (5xx/529), timeouts and connection errors. A wrong model name (404), an invalid request (400) or a bad key (401) will fail the same way every time. The SDK knows this: those three got **1 attempt each**, while an unreachable server got **3** (the default 2 retries).
- **Follow-up:** A new deploy starts returning 400s on 5% of calls. Your retry loop catches all exceptions. What happens?
- **Follow-up answer:** You multiply the load and the latency without fixing anything, and the real bug hides behind retries. Catch `BadRequestError` separately, log the request id, and fail fast so the bug surfaces.
- Notebook: [§4](notebook.ipynb#4-real-errors-and-which-ones-to-retry)

### ⭐ 4. How many retries should you configure? · Mid
- **Trap:** "As many as possible. More retries, more reliability."
- **Answer:** Retries buy reliability with time. With 17 of 40 requests hitting an injected 429/529: `max_retries=0` → **23/40 succeeded in 13.7 s**, `2` → **38/40 in 31.1 s**, `4` → **40/40 in 41.6 s**. Going from 2 to 4 retries added 10 s to save 2 requests.
- **Follow-up:** A user is waiting for a chat reply. Same setting?
- **Follow-up answer:** No. Cap retries by a time budget, not a count: a user won't wait 40 s. Use a couple of quick retries, then show a friendly "try again" or fall back. Save the high retry counts for background jobs where a slow success beats a failure.
- Notebook: [§5](notebook.ipynb#5-retries-under-failure)

### 5. You set a 2-second timeout to keep the app snappy. What breaks? · Mid
- **Trap:** "Nothing. Requests that take longer were too slow anyway."
- **Answer:** Every long answer. For a ~600-word request, the non-streaming call failed with **`APITimeoutError` at 2.04 s**. The **same 2-second timeout with streaming succeeded**, delivering **1,055 tokens over 12.2 s**, because for a stream the timeout applies to the gap between chunks, not to the whole answer.
- **Follow-up:** Why doesn't the SDK just default to a 2-second timeout?
- **Follow-up answer:** Because a blocking call legitimately takes as long as the answer is long. The default is 10 minutes, and the SDK refuses non-streaming requests that could take longer than that. Pick timeouts per route, and stream anything long.
- Notebook: [§6](notebook.ipynb#6-timeouts-streaming-vs-not)

### 6. How do you know what one call cost? · Junior
- **Trap:** "Check the billing page at the end of the month."
- **Answer:** Every response carries `usage`. A 23-token prompt with a 94-token answer cost **$0.000493** on Haiku 4.5 ($1/$5 per million input/output tokens), and the cut-off call cost **$0.000148**. Log it per call, by route, from day one.
- **Follow-up:** Output tokens cost 5× input here. What does that change in your design?
- **Follow-up answer:** Long answers dominate the bill, so ask for concise output where you can, and cap `max_tokens` per route. But watch `stop_reason` (Q1) so the cap doesn't silently cut answers.
- Notebook: [§2](notebook.ipynb#2-read-the-whole-response)

### 7. Your bug report says "the LLM call failed". What do you need to debug it? · Senior
- **Trap:** "The prompt and the error message."
- **Answer:** The **request id** (`message._request_id`, from the `request-id` header), the exception type, the status code, `stop_reason`, `usage` and the latency. The production function in §7 returns all of them. The request id is what the provider's support can trace.
- **Follow-up:** You process 1M calls a day. You can't log every prompt. What do you keep?
- **Follow-up answer:** Metadata on every call (request id, model, status or `stop_reason`, tokens, latency, retries), and full prompts only for a small sample plus every failure. That's enough to spot cut-offs, cost drift and error spikes.
- Notebook: [§7](notebook.ipynb#7-the-production-version)

### 8. Your notebook used `temperature` with the old SDK. After upgrading, the call fails before it reaches the API. Why? · Senior
- **Trap:** "The API key is wrong after the upgrade."
- **Answer:** In this environment the `anthropic` Python SDK 1.11 rejects `temperature` **client-side**: `TypeError: Messages.create() got an unexpected keyword argument 'temperature'` (found while building this notebook). Newer models steer output with the prompt and settings like effort, so the parameter isn't in the 1.x signature. (See [build #002](../02-sampling-parameters/) for what temperature does.)
- **Follow-up:** How do you upgrade an SDK in a large codebase without surprises like this?
- **Follow-up answer:** Pin the SDK version, read its migration guide and changelog before bumping the major version, and run a small integration suite against the real API (like §4 here) as part of the upgrade.
- Notebook: [§4](notebook.ipynb#4-real-errors-and-which-ones-to-retry)
