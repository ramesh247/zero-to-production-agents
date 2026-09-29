# Interview pack: tokens and embeddings

Every answer below is backed by a number from [notebook.ipynb](notebook.ipynb). Run it and you'll get the same
numbers. Token counts in sections 1–2 use GPT-4o's `o200k_base` tokenizer.

---

### 1. `"Hello"` vs `" Hello"`: are they the same token? · Junior
- **Trap:** "Yes. The tokenizer strips whitespace."
- **Answer:** No. They are different token IDs: `"Hello"` is 13225, `" Hello"` is 32949, and `"hello"` is 24912. `"HELLO"` splits into 2 tokens, and `"  Hello"` (two spaces) becomes `[220, 32949]`: one extra token for the extra space. The model sees different inputs.
- **Follow-up:** Your few-shot prompt template sometimes adds a trailing space after `Answer:`. Why could quality drift?
- **Follow-up answer:** Because `":"` followed by `" Paris"` and `": "` followed by `"Paris"` tokenize differently, the examples no longer match the pattern the model saw in training. Keep whitespace in templates identical and deterministic, and test with the model's own tokenizer.
- Notebook: [§2 Where tokenizers get weird](notebook.ipynb#2-where-tokenizers-get-weird)

### 2. How many tokens is `2026`? · Junior
- **Trap:** "One. It's a single number."
- **Answer:** Two: `202 | 6`. `1,000,000` is 5 tokens (`1 | , | 000 | , | 000`) and `0x1F4A` is 6. Numbers are split by frequency, not by place value.
- **Follow-up:** An agent compares version strings and adds up invoice totals. Where do you expect errors?
- **Follow-up answer:** Anywhere digits get chunked irregularly: the model never sees whole numbers, so arithmetic and comparisons on long numbers are fragile. Hand exact math to a tool (code execution or a calculator function) and have the model call it.
- Notebook: [§2](notebook.ipynb#2-where-tokenizers-get-weird)

### 3. Why is 🔥🚀 3 tokens and 👨‍👩‍👧 8 tokens? · Mid
- **Trap:** "Emoji are one character each."
- **Answer:** Byte-level tokenizers work on UTF-8 bytes. 👍 is common enough to be a single token, 🔥🚀 takes 3, and the family emoji is 3 people joined by zero-width joiners, which comes to **8 tokens** for one visible "character".
- **Follow-up:** Users can paste free text into your chatbot. How can someone make every request expensive?
- **Follow-up answer:** Flood the input with rare characters (emoji sequences, unusual scripts) that cost many tokens per visible character. Limit input by **tokens** counted with your model's tokenizer, not by characters.
- Notebook: [§2](notebook.ipynb#2-where-tokenizers-get-weird)

### 4. Can you estimate one model's token count with another model's tokenizer? · Mid
- **Trap:** "Close enough. Tokens are tokens."
- **Answer:** Not reliably. The same 8 English sentences cost **92 tokens** on GPT-4, GPT-4o and Qwen2.5, but **111** on XLM-R: a 21% spread. In Spanish it's **128 to 151**. The error depends on both the model and the language.
- **Follow-up:** You're building a cost dashboard across three LLM providers. How do you count?
- **Follow-up answer:** With each provider's own tokenizer or token-count endpoint, per model. Never use one proxy tokenizer for all of them, because the error isn't constant: it changes by language and content type.
- Notebook: [§3 Every model counts differently](notebook.ipynb#3-every-model-counts-differently)

### ⭐ 5. You launch your English app in Spanish with the same prompts. What happens to token cost? · Mid
- **Trap:** "Roughly the same. Spanish text is only a bit longer."
- **Answer:** Spanish is only **15% longer in characters**, but it needs **64% more tokens** on GPT-4's tokenizer (92 → 151) and **39% more** on GPT-4o's (92 → 128). You pay per token, and the context window fills per token, so the Spanish version costs and fits differently. Budget each language separately.
- **Follow-up:** You must support 10 languages on a fixed budget. What's the first lever?
- **Follow-up answer:** Measure every language with your target model's tokenizer before launch, then compare tokenizers. In this run, moving from GPT-4's tokenizer to GPT-4o's **cut Spanish from 151 to 128 tokens (−15%) while English stayed at 92**: a bigger, more multilingual vocabulary lowers non-English cost without touching English. The multilingual XLM-R tokenizer had the most even ratio (**1.24**), though it was the most expensive for English.
- Notebook: [§4 Same meaning, different price](notebook.ipynb#4-same-meaning-different-price)

### 6. Your semantic search matched "The deployment of troops failed because of a timeout in talks" to a question about a failed software deployment. What went wrong? · Senior
- **Trap:** "A cosine of 0.90 means it's relevant. Trust the score."
- **Answer:** Embeddings still leak word overlap. In this run the troops sentence scored **0.90** against "The deployment failed because of a timeout", while a real paraphrase with different words scored only **0.51**. Averaged over 3 sets, "same words, different meaning" (0.67) scored as high as true paraphrases (0.66). The 2D map shows the troops sentence sitting right on top of the software one.
- **Follow-up:** A teammate proposes a fixed cutoff: "cosine above 0.7 means relevant". Does that work?
- **Follow-up answer:** Not on this data. The relevant paraphrase (0.51) falls *below* the irrelevant look-alike (0.90), so no single threshold separates them. Calibrate on labelled pairs from your own domain, and add a second ranking stage (a reranker) rather than relying on raw cosine. That gets measured later in this series (RAG: reranking).
- Notebook: [§5 Embeddings: meaning, not words](notebook.ipynb#5-embeddings-meaning-not-words), [§7 A map of meaning](notebook.ipynb#7-a-map-of-meaning)

### 7. A user asks in Spanish; your documents are in English. Do you have to translate before retrieving? · Senior
- **Trap:** "Yes. Embeddings only match the same language."
- **Answer:** Not necessarily. With a multilingual embedding model, the Spanish translation was the **closest match of all** to its English anchor: a mean cosine of **0.87** (0.93, 0.95, 0.73) with **zero** shared words. But 0.73 on one set shows it varies.
- **Follow-up:** You need 20 languages and have a 100 ms latency budget, so there's no time for a translation step. What do you check first?
- **Follow-up answer:** Retrieval quality per language, on a small labelled set, using a multilingual embedding model. The 0.73 vs 0.95 spread here says you can't assume every language, or every sentence type, works equally well.
- Notebook: [§5](notebook.ipynb#5-embeddings-meaning-not-words)

### 8. Does the word "bank" have one embedding? · Senior
- **Trap:** "Yes. One word, one vector."
- **Answer:** The token is the same, but sentence embeddings separate the meanings. River bank vs stream bank: **0.36**. Deposit at the bank vs bank loan: **0.46**. Across meanings it drops to **0.25, 0.18, 0.06 and −0.02**. The context moves the vector.
- **Follow-up:** A user searches for the single word "bank". What should retrieval do?
- **Follow-up answer:** A one-word query has no context to pick a meaning, so expect mixed results. Use context the system already has (the user's domain, earlier turns) or ask a clarifying question, rather than trusting the top hit.
- Notebook: [§6 Context changes the vector](notebook.ipynb#6-context-changes-the-vector-bank-vs-bank)
