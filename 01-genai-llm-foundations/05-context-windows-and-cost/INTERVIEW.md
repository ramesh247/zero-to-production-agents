# Interview pack: context windows, tokens and what your prompt really costs

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb), run on **Claude Haiku 4.5**
($1 / $5 per million input / output tokens, 200K context window). Chat answers were capped at 400 output tokens,
and turns 4 and 9 hit that cap.

---

### 1. Same data, same model. Why did one prompt cost 2.4× more than another? · Junior
- **Trap:** "Tokens are just characters, so it's the same data, same cost."
- **Answer:** Format matters. The same 20 tickets took **863 tokens as CSV** and **2,091 as pretty-printed JSON**, **2.42×** as many. Pretty JSON repeats every key on every record and adds indentation, quotes and braces. Minified JSON came to **1,393**.
- **Follow-up:** Should you send everything as CSV, then?
- **Follow-up answer:** For flat, tabular data, it's the cheapest here by a wide margin. For nested data, minified JSON is the safer compromise. This notebook measured cost, not answer quality, so check that the model still reads your format correctly on your own task before switching.
- Notebook: [§1](notebook.ipynb#1-how-data-is-formatted-changes-what-it-costs)

### 2. YAML is more compact than JSON, right? · Junior
- **Trap:** "Yes. No braces, no quotes."
- **Answer:** Not here. YAML came to **1,584 tokens**, more than **minified JSON at 1,393**; only pretty-printed JSON (2,091) was worse. YAML's indentation and dash-per-record cost tokens too.
- **Follow-up:** Where does YAML still make sense?
- **Follow-up answer:** Where humans edit the text (configs, prompts you maintain by hand). For data you generate and send on every request, measure: `count_tokens` takes seconds and costs nothing per call.
- Notebook: [§1](notebook.ipynb#1-how-data-is-formatted-changes-what-it-costs)

### ⭐ 3. Your chatbot's 10th message sends 80× the input tokens of its 1st. Why? · Mid
- **Trap:** "The answers get longer as the conversation goes on."
- **Answer:** The API is **stateless**: every turn re-sends the whole conversation. Billed input went from **46 tokens on turn 1 to 3,660 on turn 10**, about 80×, while each answer stayed around 400 tokens or less. Ten turns added up to **18,441 input tokens**. The cost per turn grew less, **$0.001951 → $0.004895 (about 2.5×)**, because on Haiku the output tokens dominate the price, but the input share keeps rising with every turn.
- **Follow-up:** How do you cut that without dropping the conversation?
- **Follow-up answer:** Send less history. Keeping only the system prompt and the last 2 exchanges would have sent **7,261 input tokens, 61% fewer**. That's a token count, not a quality test: the model would lose earlier context, so summarise older turns instead of just dropping them. And cache the repeated prefix (build #006).
- Notebook: [§2](notebook.ipynb#2-chat-history-the-cost-that-compounds)

### 4. Which costs more: the prompt you send or the answer you get? · Mid
- **Trap:** "The prompt. It's usually longer."
- **Answer:** On Claude Haiku 4.5 output tokens cost **5× input tokens**. For short questions with no length instruction, output was **99.2% of the cost**. Adding "Answer in at most two sentences" cut output from **368.8 to 74.2 tokens**, cost from **$0.001859 to $0.000393** per answer, and time from **4.20 s to 1.22 s**.
- **Follow-up:** Won't short answers hurt quality?
- **Follow-up answer:** Sometimes, and that's the trade-off to measure per route. A support summary may be fine at two sentences, while a code review isn't. Set length expectations per use case, and cap `max_tokens` while watching `stop_reason` (build #003).
- Notebook: [§3](notebook.ipynb#3-output-tokens-are-the-expensive-ones)

### 5. How do you know what a request will cost before you send it? · Mid
- **Trap:** "Estimate from character count."
- **Answer:** Use `messages.count_tokens` with the same model, system prompt and messages. In this run it matched the billed input **exactly on all 10 chat turns**. It doesn't charge per call; you only pay for the real request.
- **Follow-up:** How would you use that in production?
- **Follow-up answer:** As a budget gate: count before sending, and trim history, compress data or refuse when a request would exceed the route's token budget. It turns "why was last month's bill so high" into a check you run on every request.
- Notebook: [§2](notebook.ipynb#2-chat-history-the-cost-that-compounds)

### 6. The model has a 200K-token context window. Can you just paste in all your tickets? · Senior
- **Trap:** "Yes. That's what a big context window is for."
- **Answer:** It fits more than you'd think: about **4,629 tickets as CSV, but only 1,912 as pretty JSON**. But you pay for every token, every time. A full 200K window costs **$0.20 of input per request** on Haiku 4.5.
- **Follow-up:** You need to answer 1,000 questions a day over 4,000 tickets. What do you do?
- **Follow-up answer:** Sending a full window each time would be about $200 a day in input alone. Retrieve only the tickets relevant to each question instead; that's what the RAG track in this series covers.
- Notebook: [§4](notebook.ipynb#4-what-fits-in-the-context-window)

### 7. Two chat answers came back exactly 400 tokens long. Coincidence? · Senior
- **Trap:** "The model just happened to write long answers."
- **Answer:** No. 400 was the `max_tokens` cap, and turns 4 and 9 hit it exactly, so those answers were **cut off**, with no error raised (see build #003). In a cost experiment it also means the measured history growth is slightly conservative.
- **Follow-up:** You lower `max_tokens` everywhere to save money. What do you add?
- **Follow-up answer:** Monitoring on `stop_reason == "max_tokens"` per route. A rising cut-off rate means the cap is too low for that route, and users are getting incomplete answers.
- Notebook: [§2](notebook.ipynb#2-chat-history-the-cost-that-compounds)

### 8. A sliding window saved 61% of input tokens. What did it cost you? · Senior
- **Trap:** "Nothing. The recent turns are what matter."
- **Answer:** Context. Turn 10 asked to *"summarise the whole design"*. With only the last 2 exchanges, the model wouldn't see the design decisions from turns 1–7. The notebook measured the token saving (**18,441 → 7,261**), not the answer quality, so it can't tell you how much worse those answers would be.
- **Follow-up:** How would you test that properly?
- **Follow-up answer:** Run the same conversation with full and trimmed history, then grade the answers that depend on early turns (with labels or an LLM judge, as in the evals track). Compare the quality drop with the token saving before shipping the trim.
- Notebook: [§2](notebook.ipynb#2-chat-history-the-cost-that-compounds)
