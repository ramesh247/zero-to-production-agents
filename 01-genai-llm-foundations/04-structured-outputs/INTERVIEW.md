# Interview pack: getting reliable JSON out of an LLM

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb): 20 support tickets, 6 fields each,
**Claude Haiku 4.5**, `anthropic` SDK 1.11. The retry results vary between runs (fences appear unpredictably), so
treat them as one run, not a constant. Q7 relies on the provider documentation, not on this run, and says so.

---

### 1. You asked for JSON and got JSON. Why did `json.loads` fail on every response? · Junior
- **Trap:** "The model produced broken JSON."
- **Answer:** The JSON was fine; it was **wrapped in a markdown code fence** (```` ```json ... ``` ````). That happened on **20 of 20** "Reply in JSON" responses, and on **20 of 20** even when the system prompt said "No prose, no code fences".
- **Follow-up:** So strip the fences with a regex and move on?
- **Follow-up answer:** It works: schema-in-prompt plus fence-stripping got **20/20** here. But it's a workaround that depends on the model's formatting habits staying the same. Structured outputs got **20/20** with no parsing hacks, because the API constrains the shape.
- Notebook: [§2](notebook.ipynb#2-approach-a-reply-in-json), [§3](notebook.ipynb#3-approach-b-schema-in-the-prompt--one-retry)

### 2. After stripping the fences, the JSON still failed validation. Why? · Junior
- **Trap:** "The regex is buggy."
- **Answer:** The values didn't match the contract, because the prompt never stated the contract: `"Billing"` instead of `billing`, `"High"` instead of `high`, and `"$49.99"` as a string instead of the number `49.99`. Salvaged "Reply in JSON" outputs passed validation **0/20** times.
- **Follow-up:** Can't you just lower-case everything and strip `$` in code?
- **Follow-up answer:** You'd be writing a parser for every field the model might format differently. Put the allowed values and types in a schema instead: with the schema in the prompt, the values themselves were right (once the fences were stripped, 20/20 passed).
- Notebook: [§2](notebook.ipynb#2-approach-a-reply-in-json)

### 3. Does retrying with the error message fix bad JSON? · Mid
- **Trap:** "Yes. Tell the model what's wrong and it corrects itself."
- **Answer:** Partly, and unreliably. One retry with the parse error brought schema-in-prompt from **0/20 to 10/20**; **all 10** that still failed were wrapped in code fences again. It also **doubled the calls (20 → 40)** and cost **$0.0267** against **$0.0128** for the same prompt plus fence-stripping.
- **Follow-up:** When is a retry loop still worth having?
- **Follow-up answer:** As a safety net for rare semantic failures, not as the main way to get valid output. Make the first call right, then retry only on the occasional failure, with a cap (see build #003).
- Notebook: [§3](notebook.ipynb#3-approach-b-schema-in-the-prompt--one-retry), [§5](notebook.ipynb#5-side-by-side)

### ⭐ 4. Structured outputs gave you 20/20 valid JSON. Is the data correct? · Mid
- **Trap:** "Yes. It matches the schema, so it's right."
- **Answer:** The schema guarantees the **shape**, not the **values**. The objective fields were right here (**60/60**: order id, refund amount, email). But on judgement fields it agreed with my labels on only **18/20 for priority** and **14/20 for sentiment**: valid JSON, debatable values.
- **Follow-up:** How do you catch wrong values in production?
- **Follow-up answer:** Keep a small labelled set like `data/tickets.json`, score it **field by field** whenever you change the prompt or model, and add code checks for business rules (e.g. a refund can't exceed the order total). Schema validation is the first check, not the last.
- Notebook: [§6](notebook.ipynb#6-valid-json-is-not-the-same-as-correct-data)

### 5. Is structured outputs the cheapest option? · Mid
- **Trap:** "Yes. It produces the fewest tokens."
- **Answer:** It produced the fewest **output** tokens (**47** on average, against **68** for schema-in-prompt), but it cost slightly more overall: **$0.0157 vs $0.0128** for 20 tickets against schema-in-prompt plus fence-stripping. You pay a little for the guarantee.
- **Follow-up:** At 1M tickets a day, does that difference matter?
- **Follow-up answer:** It's about **$0.000145 per ticket**, roughly **$145 a day** at that volume. Compare it with what one malformed record costs you downstream (a failed job, a wrong refund, an on-call page) and decide per route.
- Notebook: [§5](notebook.ipynb#5-side-by-side)

### 6. The first structured-output call was twice as slow as the rest. Why? · Senior
- **Trap:** "Network jitter."
- **Answer:** A new schema is compiled on first use and then cached (for 24 hours, per the docs). In this run the first call took **1.98 s** against a **0.93 s** median for the other 19.
- **Follow-up:** Your app builds a slightly different schema per customer. What happens?
- **Follow-up answer:** Every new schema pays the compile cost. Keep schemas stable and few: one schema per task, with customer-specific details in the prompt rather than in the schema.
- Notebook: [§4](notebook.ipynb#4-approach-c-structured-outputs)

### 7. Your schema says `refund_amount` must be ≥ 0. Will the API enforce it? · Senior
- **Trap:** "Yes. It's standard JSON Schema (`minimum: 0`)."
- **Answer:** Per the provider documentation (not this run), structured outputs don't support numeric constraints like `minimum` and `maximum`, or string-length constraints. The Python SDK removes them from the schema it sends and **validates them client-side**, so a violation becomes a validation error in your code, not something the model is prevented from generating.
- **Follow-up:** Where should business rules live, then?
- **Follow-up answer:** In code, after parsing, next to the field-level checks from Q4. The schema covers types and allowed values; your code covers the rules.
- Notebook: [§1](notebook.ipynb#1-the-task-and-the-schema)

### 8. One ticket is in Spanish. Do you need a separate pipeline? · Senior
- **Trap:** "Yes. Translate it first."
- **Answer:** Not for this task. The Spanish ticket (*"me cobraron 15 dólares de más en el pedido ORD-33091"*) went through the same structured-output call, and the order id, the refund amount of **15** and the email all came out right. All **60/60** objective fields were correct across the 20 tickets.
- **Follow-up:** What changes when 40% of your traffic isn't in English?
- **Follow-up answer:** Correctness may hold, but cost won't: the same meaning takes more tokens in many languages (build #001 measured +39% to +64% for Spanish, depending on the tokenizer). Include those languages in your labelled set, and budget tokens per language.
- Notebook: [§6](notebook.ipynb#6-valid-json-is-not-the-same-as-correct-data)
