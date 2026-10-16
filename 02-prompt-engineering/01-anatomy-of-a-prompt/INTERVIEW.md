# Interview pack: anatomy of a production prompt

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb), run on **Claude Haiku 5.5** with thinking off.
The task: label support tickets with category, priority and sentiment. Six prompts, 3 runs each, on a **dev set**
(the 20 tickets from build #004, which the rubric was written from) and a held-out **test set** (12 new tickets, labelled
with the rubric before any model run). "All 3 right" means all three labels matched mine.

| Prompt | Dev: all 3 right | Test: all 3 right | Usable replies (dev / test) |
|---|---|---|---|
| A: task only | 13% (8/60) | 19% (7/36) | 25% / 33% |
| B: + format | 55% | 42% | 100% / 100% |
| C: + context | 85% | 75% | 100% / 100% |
| D: + role (full prompt) | 87% (52/60) | 75% (27/36) | 100% / 100% |
| D without context | 68% | 47% | 100% / 100% |
| D without format | 50% | 67% | 57% / 75% |

---

### 1. Which part of a prompt matters most: role, context, task or format? · Junior
- **Trap:** "The role. 'You are an expert…' is what makes it work."
- **Answer:** The role mattered least. Adding it moved "all 3 right" by **+2 points on dev (1 run out of 60) and 0 on test**. Adding the output format gave **+42 / +23 points**, and adding context (my labelling rubric) **+30 / +33**.
- **Follow-up:** So should you delete roles from your prompts?
- **Follow-up answer:** For classification like this, it didn't earn its tokens. The notebook didn't test tasks where tone matters, like writing the reply to the customer, so test it there before dropping it.
- Notebook: [§5](notebook.ipynb#5-what-each-part-is-worth)

### 2. With only the task in the prompt, the model scored 13%. Was it bad at triage? · Junior
- **Trap:** "Yes. It needs a smarter model."
- **Answer:** Mostly it was unreadable, not wrong. **75% of its replies on dev couldn't be parsed** into one value per field: long markdown answers like "Billing / Refund (duplicate charge)" and "neutral to mildly negative". When it could be parsed, it used *its own* definitions: it called a double charge **medium** priority, where my rubric says **high**.
- **Follow-up:** Which fix comes first?
- **Follow-up answer:** The format. It took usable replies from 25% to 100% and output from 178 to 29 tokens per ticket. Then context, so the labels mean what your team means.
- Notebook: [§4](notebook.ipynb#4-one-ticket-six-prompts)

### ⭐ 3. The model's answer was right, but your pipeline rejected it. How? · Mid
- **Trap:** "It can't happen. Right is right."
- **Answer:** The full prompt without the format line answered ticket 1 correctly (billing, high, neutral), then explained itself: *"sentiment is neutral rather than negative"*. A program now sees two sentiments. Without the format, only **57% of replies on dev were usable (75% on test)**, so "all 3 right" fell from 87% to 50% on dev.
- **Follow-up:** You need the explanation too. What do you do?
- **Follow-up answer:** Ask for it as a field in the JSON (`"reason": "..."`), so it's separate from the labels. Or use structured outputs (build #004), which guarantee the shape.
- Notebook: [§4](notebook.ipynb#4-one-ticket-six-prompts)

### 4. You wrote the rubric by looking at the dev tickets. Isn't +30 points just overfitting? · Mid
- **Trap:** "Probably, but it's still an improvement."
- **Answer:** That's what the held-out test set checks. The 12 test tickets were new and labelled with the rubric **before** any model run. Context still added **+33 points there (42% → 75%)**, and removing it from the full prompt cost **28 points on test**, more than on dev (19). The rubric carries information the model can't guess.
- **Follow-up:** How do you keep that honest as the rubric grows?
- **Follow-up answer:** Keep a held-out set you never tune on, label it before reading model outputs, and add new edge cases to it whenever production surprises you.
- Notebook: [§1](notebook.ipynb#1-the-data-a-dev-set-and-a-held-out-test-set), [§5](notebook.ipynb#5-what-each-part-is-worth)

### 5. The rubric made the prompt 3× longer. Did it make it 3× more expensive? · Mid
- **Trap:** "Yes. You pay per token."
- **Answer:** Input went from about **168 to 526 tokens**, and the cost per 1,000 tickets from **$0.031 to $0.067**. But the cheapest-looking prompt, task only (74 input tokens), was the most expensive at **$0.097 per 1,000**, because it wrote 178 output tokens per ticket and output costs 5× input.
- **Follow-up:** At 10 million tickets a month, would you cache the rubric?
- **Follow-up answer:** Measure first. At about 500 tokens, the prefix may be under the model's minimum cacheable length, and caching it would then do nothing (build #006). Check `cache_read_input_tokens` on the second call.
- Notebook: [§3](notebook.ipynb#3-run-them)

### 6. The full prompt still misses on 25% of test runs. Where? · Senior
- **Trap:** "Use a bigger model."
- **Answer:** On rubric edge cases, not random tickets. On test: the sentiment of a calm "charged twice… please fix", the sentiment of a "minor thing" display bug, and the priority of an iOS login failure with a working desktop fallback (my rubric says medium, because there's a workaround). Across both sets, every miss was a single field, on 7 of the 32 tickets.
- **Follow-up:** How do you fix edge cases like these?
- **Follow-up answer:** Show the model a worked example of each, which is the next build (#010: zero-shot vs few-shot). And check the rubric itself: if a careful human would hesitate on a ticket, the definition needs work, not the model.
- Notebook: [§5](notebook.ipynb#5-what-each-part-is-worth)

### 7. Your PM wants to add "You are a world-class support expert. Be accurate." Will it help? · Senior
- **Trap:** "It can't hurt, and it might help."
- **Answer:** Not measurably. A role added **1 correct run out of 60 on dev and 0 out of 36 on test**. Instructions that don't carry information ("be accurate") give the model nothing new. The rubric did, with definitions like "charged twice for the same order = high", which is why it moved the score by 30+ points.
- **Follow-up:** How do you push back without sounding dismissive?
- **Follow-up answer:** Run it. An A/B on the same test set takes minutes and costs cents. Then the decision is about a number, not an opinion.
- Notebook: [§5](notebook.ipynb#5-what-each-part-is-worth)

### 8. Is a 2-point gain real or noise? · Senior
- **Trap:** "Any gain is a gain."
- **Answer:** Here, 2 points on dev is **1 run out of 60**. That's within what a re-run could change, so treat it as no difference. The format and context gains (23-42 points, dozens of runs) are far too big to be noise.
- **Follow-up:** How would you measure small gains reliably?
- **Follow-up answer:** More tickets, more runs, and a fixed test set. Build #014 in this series turns that into a repeatable eval loop.
- Notebook: [§3](notebook.ipynb#3-run-them)
