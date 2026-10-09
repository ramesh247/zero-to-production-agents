# Interview pack: prompt caching

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb), run on **Claude Haiku 4.5**
(per million tokens: input $1.00, cache write $1.25 with the 5-minute TTL, cache read $0.10, output $5.00).
The main test is a support assistant with a **7,928-token** system prompt (a 150-product catalog) answering 10 questions.

---

### 1. You added `cache_control` and nothing changed. Why? · Junior
- **Trap:** "Caching takes a few requests to warm up."
- **Answer:** The prompt was too short. A **2,971-token** prompt marked for caching was sent 3 times: **0 tokens written, 0 read**, no error and no warning. Claude Haiku 4.5 only caches a prefix of **4,096 tokens or more**; below that the marker is silently ignored.
- **Follow-up:** How would you catch this in production?
- **Follow-up answer:** Log `usage.cache_creation_input_tokens` and `usage.cache_read_input_tokens` on every response, and alert when a route that should cache shows zero reads. The minimum differs by model, so re-check it when you switch models.
- Notebook: [§2](notebook.ipynb#2-silent-failure-1-too-short-to-cache)

### 2. Is the first cached request cheaper? · Junior
- **Trap:** "Yes, that's the point of caching."
- **Answer:** No, it costs more. The first call **writes** the cache at 1.25× the input price: **$0.0101**, against an average of **$0.0084** for an uncached call. Every call after that **reads** at 0.1×: around **$0.001** each.
- **Follow-up:** So when does caching start paying off?
- **Follow-up answer:** On the second request within the TTL. For the cached part of the prompt: 2 requests cost 1.35 units cached vs 2.0 uncached (32% less), 10 cost 2.15 vs 10 (78% less). One request on its own costs 25% more.
- Notebook: [§3](notebook.ipynb#3-caching-done-right-10-questions-cached-vs-not), [§5](notebook.ipynb#5-when-does-caching-pay-off)

### ⭐ 3. You put the current time at the top of your system prompt. What does that do to caching? · Mid
- **Trap:** "Nothing. It's one line."
- **Answer:** It breaks it, silently. Caching is a **prefix match**: any byte that changes before the cache breakpoint means a miss. With a timestamp, all 5 calls **wrote** a fresh 7,941-token cache and **none read** one. Input cost for 5 questions: **$0.0497 with the timestamp**, **$0.0397 with no caching at all** (25% more) and **$0.0132 with caching done right**.
- **Follow-up:** You still need the model to know the time. Where does it go?
- **Follow-up answer:** After the cached part: in the user message, or in a system block placed after the breakpoint. Or round it (the date, not the microsecond) so it changes once a day. Same rule for request ids, user names, and JSON you serialise without sorting keys.
- Notebook: [§4](notebook.ipynb#4-silent-failure-2-one-timestamp-breaks-it)

### 4. How much did caching save on 10 questions? · Mid
- **Trap:** "90%. Cache reads are 10% of the price."
- **Answer:** **78% of the input cost** ($0.0794 → $0.0172), not 90%, because the first call pays the 1.25× write. On the total bill it was **74%** ($0.0836 → $0.0216), because output tokens (about 850 per run) aren't cached and cost the same either way.
- **Follow-up:** How do you get closer to 90%?
- **Follow-up answer:** More reads per write. The write is paid once per TTL window, so the more requests share it, the closer you get to 0.1×: the arithmetic gives 89% at 100 requests.
- Notebook: [§3](notebook.ipynb#3-caching-done-right-10-questions-cached-vs-not), [§5](notebook.ipynb#5-when-does-caching-pay-off)

### 5. Does prompt caching make responses faster? · Mid
- **Trap:** "Yes, always. It skips the prompt."
- **Answer:** It depends on the size. With the **8K-token** prompt, median time to first text didn't move (**0.444 s vs 0.450 s**). With a **52K-token** prompt, the median went from **0.80 s to 0.56 s**. But that's 5 calls each way, and single uncached calls ranged from 0.43 s to 1.00 s, so treat it as a direction, not a benchmark.
- **Follow-up:** If caching doesn't speed up a short prompt, what does?
- **Follow-up answer:** Shorter outputs and streaming (builds #003 and #005). For a short prompt, generating the answer is most of the time.
- Notebook: [§3](notebook.ipynb#does-it-make-responses-faster)

### 6. What exactly gets cached, and where do you put the breakpoint? · Senior
- **Trap:** "The system prompt gets cached, whatever is in it."
- **Answer:** The whole prefix up to the breakpoint, in order: tools, then system, then messages. Put the breakpoint at the end of what's stable (the catalog and the policies) and everything that changes (the question, the time, the user) after it. In the notebook only the question changes: 13-20 input tokens per call were billed at full price and 7,921 came from the cache.
- **Follow-up:** You add one tool to the agent. What happens to the cache?
- **Follow-up answer:** Tools come first in the prefix, so changing them invalidates everything after: the next call writes a new cache. Keep tool definitions stable and in a fixed order.
- Notebook: [§3](notebook.ipynb#3-caching-done-right-10-questions-cached-vs-not)

### 7. Your app sends the same prompt once every 10 minutes. Should you cache it? · Senior
- **Trap:** "Yes, it's the same prompt every time."
- **Answer:** Not with the default 5-minute TTL. The cache expires between requests, so every call pays the **1.25× write and never reads**, which is 25% more than not caching (like the timestamp case in §4). The 1-hour TTL writes at 2× and reads at 0.1×: 6 requests an hour would cost 2 + 5 × 0.1 = 2.5 units instead of 6. That's arithmetic from the prices; the notebook measured only the 5-minute TTL.
- **Follow-up:** What does a cache read do to the TTL?
- **Follow-up answer:** It refreshes it. A route that gets a request every few minutes keeps its cache warm on the 5-minute TTL for free; it's sparse traffic that needs the 1-hour TTL.
- Notebook: [§5](notebook.ipynb#5-when-does-caching-pay-off)

### 8. Why does the notebook put a random run id at the start of the system prompt? · Senior
- **Trap:** "It doesn't matter for caching."
- **Answer:** To make the first call a guaranteed **write**. The cache matches on the exact prefix, so re-running the notebook within 5 minutes would otherwise find the previous run's cache, and "call 1" would show reads. The run id is a deliberate cache-buster, exactly what you must *not* do by accident in production.
- **Follow-up:** Where else do accidental cache-busters hide?
- **Follow-up answer:** Anything generated per request that lands before the breakpoint: timestamps, UUIDs, a user's name in the system prompt, `json.dumps` without `sort_keys=True`, tool lists built from a set. If reads drop to zero after a deploy, diff two consecutive request prefixes.
- Notebook: [setup](notebook.ipynb#1-the-setup-an-8k-token-catalog-prompt)
