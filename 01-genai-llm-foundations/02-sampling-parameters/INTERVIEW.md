# Interview pack: temperature, top-p, top-k

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb), run on Qwen2.5-0.5B (vocabulary: 151,665
tokens). Other models give different numbers but the same shapes. Q8 relies on provider documentation, not on this run, and says so.

---

### 1. What does temperature = 0 actually do? · Junior
- **Trap:** "It makes the model more accurate."
- **Answer:** It makes it **greedy**: it always picks the single most likely token. In this run, all 10 samples were identical and the text looped ("Write clean code by following the…" for tip after tip). Repeat-4 was **0.22**, against **0.01** at T=0.7. It's predictable, not more correct.
- **Follow-up:** You need reproducible outputs for tests but don't want the loops. What do you do?
- **Follow-up answer:** Use sampling with a **fixed seed**. Note that even T=0.3 gave **10 different completions out of 10** here, so a "low temperature" setting is not the same as deterministic. If you need repeatability, fix the seed, and keep greedy for tasks with one canonical answer.
- Notebook: [§4](notebook.ipynb#4-same-prompt-8-settings-10-samples-each)

### 2. Does a higher temperature let the model use new words? · Junior
- **Trap:** "Yes. It unlocks more of the vocabulary."
- **Answer:** No. It only **re-weights** the probabilities the model already has. What changes is how many tokens share the probability: covering 90% of it took **2 tokens at T=0.2, 12 at T=0.7, 77 at T=1.0, 5,951 at T=1.5 and 35,971 at T=2.0**.
- **Follow-up:** Why does that matter for output quality?
- **Follow-up answer:** At T=1.5 the top token fell from 18.1% to **5.3%**, and most of the probability moved to tokens the model considered unlikely. The generated text turned into multilingual noise (avg logprob **−9.83**, against −2.23 at T=0.7).
- Notebook: [§2](notebook.ipynb#2-temperature-reshapes-the-menu)

### 3. top-k vs top-p: what's the difference? · Mid
- **Trap:** "They're two ways of doing the same thing."
- **Answer:** top-k always keeps a fixed number of tokens. top-p keeps however many it takes to reach probability p, so it **adapts to how sure the model is**. At T=0.7, top-p=0.9 kept **8** tokens for "The capital of France is" but **115** for "My favourite thing to cook on weekends is". top-k=50 keeps 50 in both cases.
- **Follow-up:** Which one would you pick for a chatbot that handles both factual and creative questions?
- **Follow-up answer:** top-p, because it narrows itself on confident steps and widens on open ones. A fixed k is either too loose for factual questions (8 candidates were enough for France, k=50 adds 42 more) or too tight for creative ones (115 > 50).
- Notebook: [§3](notebook.ipynb#3-top-k-vs-top-p-who-gets-to-stay)

### ⭐ 4. You set top-p = 0.9 as a safety net, so T = 1.5 is safe, right? · Mid
- **Trap:** "Yes. top-p cuts off the long tail."
- **Answer:** No. Temperature is applied **first**, so the menu is already flat when top-p runs. With top-p=0.9 at T=1.5, the model still had **5,351** candidate tokens for the France prompt and **10,995** for the cooking prompt. The text was gibberish either way: avg logprob **−8.52** with top-p, against −9.83 without it and −2.53 at T=1.0 with top-p.
- **Follow-up:** Product wants "more creative" answers. What do you change?
- **Follow-up answer:** Stay around T=0.7–1.0, and ask for variety in the prompt instead of raising the temperature. T=0.7 already gave **10 of 10 distinct completions**, distinct-2 of **0.81** and almost no repetition (0.01), with readable text (logprob −2.23).
- Notebook: [§3](notebook.ipynb#3-top-k-vs-top-p-who-gets-to-stay), [§4](notebook.ipynb#4-same-prompt-8-settings-10-samples-each)

### 5. The model says the best language for beginners is C. Is that its opinion? · Mid
- **Trap:** "Yes. The top token is the model's answer."
- **Answer:** It's only the most frequent continuation, and a weak one: **' C' 18.1%, ' Python' 11.9%, ' Java' 8.2%**, plus blank lines like `' __'` at 6.7%, picked up from fill-in-the-blank quiz text. A base model predicts text; it doesn't hold views. An 18% top token means it's very unsure.
- **Follow-up:** Can you use the top token's probability as a confidence score?
- **Follow-up answer:** As a rough signal, yes: at the same T=1.0, the top token gets **31.6%** for "The capital of France is" against **18.1%** here. But it measures how predictable the next token is, not whether the claim is true, so calibrate it on labelled examples before trusting it.
- Notebook: [§1](notebook.ipynb#1-the-models-real-menu), [§3](notebook.ipynb#3-top-k-vs-top-p-who-gets-to-stay)

### 6. Your agent repeats the same step over and over at temperature 0. Why? · Senior
- **Trap:** "The model is broken. Use a bigger one."
- **Answer:** Greedy decoding always takes the most likely continuation, and once text starts repeating, repeating becomes the most likely continuation. Here, greedy hit repeat-4 = **0.22** while every sampled setting at T≥0.7 stayed at **0.00–0.01**.
- **Follow-up:** You need the agent's step choices to stay predictable. How do you stop the loops without random output?
- **Follow-up answer:** Treat it as a control problem, not a sampling one: cap the number of steps, detect repeated actions, and feed back "you already tried X". Moving to T=0.3 alone wouldn't give predictability: it produced 10 different completions out of 10 in this run.
- Notebook: [§4](notebook.ipynb#4-same-prompt-8-settings-10-samples-each)

### 7. How do you choose a temperature with data instead of gut feel? · Senior
- **Trap:** "Use 0.7. Everyone does."
- **Answer:** Measure variety against readability on your own prompts. Here: T=0.7 had distinct-2 **0.81** and logprob **−2.23**; T=1.0 had **0.99** and **−4.28** (more varied, much stranger); top-k=20 at T=1.0 had **0.87** and **−2.34**. The right setting depends on how much strangeness your task can tolerate.
- **Follow-up:** You run 1M requests a day. How do you keep that choice honest?
- **Follow-up answer:** Log a sample of outputs per setting and track the same cheap metrics (distinct-n, repetition, the model's own logprob) plus a task-quality check, then re-run the comparison whenever you change models. The numbers are model-specific.
- Notebook: [§4](notebook.ipynb#4-same-prompt-8-settings-10-samples-each)

### 8. Your code sets temperature=0, and the new model's API rejects it. What now? · Senior
- **Trap:** "It's an SDK bug. Pin an older version."
- **Answer:** It's deliberate. Per the provider documentation (not this run), several current hosted models, including Claude Opus 5.5 and Sonnet 5.5, reject `temperature`, `top_p` and `top_k` with an error. They're steered with the prompt and settings like reasoning effort instead.
- **Follow-up:** Your app relied on T=0 for consistent JSON. How do you migrate?
- **Follow-up answer:** Use structured outputs or schema validation for the format, and test for consistency on the new model rather than assuming it. As Q1 showed, sampling settings never guaranteed it.
- Notebook: [§5](notebook.ipynb#5-when-you-cant-set-temperature-at-all)
