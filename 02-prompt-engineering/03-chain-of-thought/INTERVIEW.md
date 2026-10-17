# Interview pack: chain-of-thought and extended thinking

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb), run on **Claude Haiku 5.5**.
Task A: 20 questions over build #006's 150-product catalog (16 need counting across rows, 4 are lookups), 3 runs each.
Task B: build #010's 20 fresh support tickets with rubric v2, 3 runs each. The catalog was prompt-cached.

| Setting (task A) | All 20 questions | Counting (48 runs) | Avg output tokens | Median s | $ per 1,000 questions |
|---|---|---|---|---|---|
| Answer only (thinking off) | 78% | 73% | 877 | 2.52 | $0.567 |
| "Think step by step" (thinking off) | 78% | 73% | 1,069 | 3.08 | $0.645 |
| Thinking, effort low | 97% | 96% | 956 | 2.79 | $0.607 |
| Thinking, effort medium (default) | 100% | 100% | 1,050 | 3.51 | $0.634 |
| Thinking, effort high | 100% | 100% | 1,166 | 3.49 | $0.692 |

---

### 1. Does "think step by step" make the model more accurate? · Junior
- **Trap:** "Yes. It's the classic chain-of-thought trick."
- **Answer:** Not here. On the 16 counting questions, "think step by step" scored **73%**, exactly the same as asking for the answer only. Turning on the model's built-in thinking scored **96-100%**.
- **Follow-up:** So is prompted chain-of-thought useless?
- **Follow-up answer:** On a model with built-in thinking, it was redundant in this run. It can still help on models without a thinking mode, or when you need the reasoning visible to a user. Measure it on your model.
- Notebook: [§3](notebook.ipynb#3-task-a-catalog-questions)

### ⭐ 2. You told the model "reply with only the answer". Why did it write 3,251 tokens? · Mid
- **Trap:** "It ignored the instruction. Bad model."
- **Answer:** On hard counting questions, Haiku 5.5 with thinking off reasoned in its visible reply anyway: **1,093 output tokens on average** for counting questions vs **12 for lookups**, with the same "answer only" prompt. So "answer only" and "think step by step" were really the same experiment, and both scored **73%**. What changed the score was *where* the reasoning happened: built-in thinking got **100%** at effort medium, for a similar token count (1,303 vs 1,305).
- **Follow-up:** Your parser expected a bare number. What breaks?
- **Follow-up answer:** Anything that reads the whole reply as the answer. Ask for the answer in tags (`<answer>…</answer>`) or use structured outputs, so the reasoning can't leak into the value.
- Notebook: [§4](notebook.ipynb#4-lookups-vs-counting)

### 3. Extended thinking must be much more expensive, right? · Mid
- **Trap:** "Yes. Thinking tokens are billed as output."
- **Answer:** Not on this task. Because the "answer only" setting already wrote ~1,100 tokens of visible working on counting questions, thinking at effort medium cost about the same: **$0.634 vs $0.567 per 1,000 questions**, for 100% instead of 78%. Median time went from 2.52 s to 3.51 s.
- **Follow-up:** When would thinking be clearly more expensive?
- **Follow-up answer:** On tasks where the model would otherwise answer in a few tokens, like the ticket triage in §5: there it doubled the cost per ticket.
- Notebook: [§3](notebook.ipynb#3-task-a-catalog-questions)

### 4. Which effort level would you ship? · Mid
- **Trap:** "High. Maximum accuracy."
- **Answer:** Medium, the default. On counting questions: low **96%** (46/48), medium **100%**, high **100%**. High produced about 11% more output tokens than medium (1,442 vs 1,303) for no measurable gain.
- **Follow-up:** And if a 4% error rate were acceptable?
- **Follow-up answer:** Then low saves a little: $0.607 vs $0.634 per 1,000 questions here. Small savings, real misses, so it depends on what a wrong count costs you.
- Notebook: [§3](notebook.ipynb#3-task-a-catalog-questions)

### 5. Does thinking slow down easy questions too? · Junior
- **Trap:** "Yes, it thinks on everything."
- **Answer:** Barely. Thinking is adaptive: on the 4 lookups, effort low used **12 output tokens and 0.61 s** (no thinking), medium **39 tokens and 0.77 s**. Across all 20 questions, effort low thought on 80% of calls and medium on 90%.
- **Follow-up:** So you can leave it on everywhere?
- **Follow-up answer:** For mixed traffic, adaptive thinking mostly handles it. But check tasks that never need it (§5), where it still added tokens and time.
- Notebook: [§4](notebook.ipynb#4-lookups-vs-counting)

### 6. Should you turn on thinking for ticket triage? · Senior
- **Trap:** "Yes. Reasoning always helps."
- **Answer:** No. On the 20 fresh tickets: answer only **87%** (52/60), "think step by step" **83%**, thinking at medium **83%**. Reasoning cost more (**$0.084 → $0.170 and $0.136** per 1,000 tickets) and took longer (**0.73 s → 1.50 s and 1.11 s** median) for a slightly lower score.
- **Follow-up:** What does that tell you about where reasoning helps?
- **Follow-up answer:** It helps when the answer needs steps (counting, combining rows). Triage is matching a ticket to written rules, and the rules were already in the prompt. Build #008 found the same split.
- Notebook: [§5](notebook.ipynb#5-task-b-ticket-triage)

### 7. Visible reasoning and built-in thinking used about the same tokens. Why such different accuracy? · Senior
- **Trap:** "Tokens are tokens. They should score the same."
- **Answer:** The notebook can't see inside the model, so it can't tell you why. It shows that the token count alone didn't explain accuracy: on counting questions, **1,305 tokens of visible step-by-step working scored 73%** and **1,303 tokens with built-in thinking scored 100%**. The visible replies also made mistakes you can read, like counting 41 Android products where the answer is 52.
- **Follow-up:** How would you use the visible reasoning, then?
- **Follow-up answer:** As a debugging aid, not as a quality lever: it shows *where* a count went wrong. For accuracy, use the thinking mode and keep the reply short.
- Notebook: [§4](notebook.ipynb#4-lookups-vs-counting)

### 8. Product wants these catalog answers in under 1 second. What do you say? · Senior
- **Trap:** "Turn thinking off. It's faster."
- **Answer:** Thinking off doesn't make it both fast and right. Counting questions took a **median of 3.2 s even with thinking off** (the model reasoned in its reply) and scored 73%. Only lookups came in under a second (0.6-0.8 s).
- **Follow-up:** So what's the design?
- **Follow-up answer:** Let code do the counting: give the model a tool that runs the filter and returns the number (build #008's conclusion too), and keep the model for understanding the question. That's the agents subject, later in this series.
- Notebook: [§4](notebook.ipynb#4-lookups-vs-counting)
