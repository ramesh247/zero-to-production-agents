# Interview pack: choosing a model

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb). Five setups, each **at its default settings**
unless the name says otherwise: Claude Haiku 4.5, Claude Haiku 5.5, Claude Haiku 5.5 with thinking off, Claude Sonnet 5.5
and Claude Opus 5.5. Three tasks with known answers: 20 support tickets (build #004), a 300×375 invoice image
(build #007, 3 runs) and 10 counting questions over a 150-product catalog (build #006, 3 runs). The whole run cost $0.98.

---

### 1. Is the most expensive model the most accurate? · Junior
- **Trap:** "Yes, that's what you're paying for."
- **Answer:** Not on every task. On ticket extraction, **all five setups got 60/60** objective fields (order id, refund amount, email). The cost per 1,000 tickets ranged from **$0.10 on Haiku 5.5 to $3.82 on Opus 5.5**, 38× more for the same score.
- **Follow-up:** So always use the cheapest?
- **Follow-up answer:** Use the cheapest one that passes *your* test. On the small invoice image, Opus was the only one at 62/62 on every run. The answer is per task, which is why you measure per task.
- Notebook: [§2](notebook.ipynb#2-task-a-ticket-extraction), [§5](notebook.ipynb#5-the-scorecard)

### ⭐ 2. The cheapest model tied the most expensive one on counting questions. Then you changed one setting and it scored 5/30. What changed? · Mid
- **Trap:** "The model got worse at random."
- **Answer:** Thinking. With its default thinking on, Claude Haiku 5.5 got **30/30**, the same as Sonnet 5.5 and Opus 5.5. With thinking off, it got **5/30**, and Claude Haiku 4.5 (which doesn't think by default) got **4/30**. Counting and summing across 150 rows needs working-out; without it, every model guessed.
- **Follow-up:** Then why turn thinking off in build #007?
- **Follow-up answer:** Because reading values off an invoice isn't reasoning. On this run's invoice task, thinking off read 56-57/62 and thinking on 54-62: no clear gain, at 2.6× the output tokens. Thinking pays where the task needs steps, not everywhere.
- Notebook: [§4](notebook.ipynb#4-task-c-questions-that-need-counting)

### 3. What did that thinking cost? · Mid
- **Trap:** "Nothing, it's the same model."
- **Answer:** Time and output tokens. On the catalog questions Haiku 5.5 with thinking produced **11,295 output tokens per call on average vs 177** without, and took a **38.9 s median vs 1.6 s**. It was still cheap: **$0.0067 per call**, against **$0.0815 for Sonnet 5.5** and **$0.1305 for Opus 5.5** for the same 10/10.
- **Follow-up:** Haiku 5.5 was slower than Opus here. How?
- **Follow-up answer:** It thought longer: 11,295 output tokens vs Opus's 4,340. A cheap model can spend more tokens reaching the same answer. Measure latency per task, not per model.
- Notebook: [§4](notebook.ipynb#4-task-c-questions-that-need-counting)

### 4. A bigger model will agree with your labels more often, right? · Mid
- **Trap:** "Yes, it understands the tickets better."
- **Answer:** No. On category, priority and sentiment, agreement with my labels was **51-53 out of 60 for every setup**, a spread of 2. These fields are judgement calls (is a ticket "high" or "urgent"? is a polite complaint "neutral" or "negative"?), so the gap is about definitions, not reading ability.
- **Follow-up:** How do you fix that?
- **Follow-up answer:** Define the labels better: write down what "urgent" means, with examples, and put it in the prompt. A clearer rubric moves every model; a bigger model doesn't fix an ambiguous one.
- Notebook: [§2](notebook.ipynb#2-task-a-ticket-extraction)

### 5. You need to read small images reliably. Do you pay for Opus? · Senior
- **Trap:** "Yes. Only Opus got 62/62."
- **Answer:** Maybe not. At 300×375, Opus 5.5 read **62/62 on all 3 runs**, Sonnet 5.5 59-62, Haiku 5.5 54-62, and Haiku 4.5 only **4-8**. But build #007 showed Haiku 5.5 read the same invoice **62/62 at 400×500**, for 833 input tokens. Sending a slightly bigger image is cheaper than a bigger model.
- **Follow-up:** And if you can't control the image size?
- **Follow-up answer:** Then the model is your lever: per invoice here, Opus cost about $0.032 and Haiku 5.5 about $0.001. Whether that's worth it depends on what a misread number costs you.
- Notebook: [§3](notebook.ipynb#3-task-b-a-small-invoice-image)

### 6. Why did Haiku 4.5 use 8,325 input tokens for the catalog and the others 10,916? · Senior
- **Trap:** "Different system prompts."
- **Answer:** Different tokenizers. The newer models count the same text as **31% more tokens**. So a price per token isn't a price per task: Haiku 5.5 is a tenth of Haiku 4.5's price per token, but the same prompt has more tokens.
- **Follow-up:** How do you compare costs fairly then?
- **Follow-up answer:** Run the real task and compare the bill, as this notebook does, or use `count_tokens` with each model. Never take a token count measured on one model and reuse it on another.
- Notebook: [§4](notebook.ipynb#4-task-c-questions-that-need-counting)

### 7. The catalog feature has a 3-second latency budget. Which model do you pick? · Senior
- **Trap:** "Opus. It got 30/30."
- **Answer:** None of them meets it at full accuracy. Every setup that scored 30/30 had a **median of 33-39 s**. The ones under 3 s (Haiku 4.5, Haiku 5.5 thinking off) scored **4-5/30**.
- **Follow-up:** So what do you do?
- **Follow-up answer:** Stop asking a model to count rows. Give it a tool (a SQL query or a Python function) that does the counting, and let the model pick the filter. That's tool use, the next subject in this series. I haven't measured it here.
- Notebook: [§4](notebook.ipynb#4-task-c-questions-that-need-counting)

### 8. How would you choose a model for a new feature? · Senior
- **Trap:** "Pick the best model on the leaderboard."
- **Answer:** Build a small test set with known answers for *that* feature, run the cheap models first, and only move up where they fail. In this run, the right choice changed per task: Haiku 5.5 with thinking off for extraction, Haiku 5.5 with thinking on for counting (if latency allows), and Opus or a bigger image for small text.
- **Follow-up:** How big does the test set need to be?
- **Follow-up answer:** Big enough to see the differences you care about. 20 tickets showed no difference between models; 3 invoice runs showed Haiku 5.5 ranging from 54 to 62. Small differences need more runs, which is the evals subject later in this series.
- Notebook: [§5](notebook.ipynb#5-the-scorecard)
