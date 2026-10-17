# Interview pack: 7 prompt anti-patterns

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb), run on **Claude Haiku 5.5** with thinking off,
on build #014's 20 test tickets (labelled before any model run), 3 runs each. The "fix" for the labelling tasks is
build #014's best prompt (rubric v3 plus a calm JSON format line).

| Anti-pattern | Anti-pattern result | Fix result |
|---|---|---|
| 1. Vague task ("What do you think?") | 2% usable, 0% right, 362 output tokens | 100% usable, 90% right, 30 tokens |
| 2. Conflicting instructions (under 50 words vs "in detail") | 67% under 50 words, max 83 | 82% under 50 words, max 56 |
| 3. SHOUTING ("IMPORTANT!!! … CRITICAL!!!") | 100% usable, 85% right | 100% usable, 90% right |
| 4. Only "Don't use markdown" | 5% of replies with markdown (no instruction: 20%) | 0% (positive instruction) |
| 5. A broken format example (single quotes, trailing comma) | 25% valid JSON | 100% |
| 6. 10K tokens of unrelated catalog | 90% right, $1.113 per 1,000 tickets | 90% right, $0.085 |
| 7. Trusting a self-reported confidence | right answers averaged 88.5, wrong 82.5 | (see question 7) |

---

### 1. Which anti-pattern did the most damage? · Junior
- **Trap:** "Shouting, or a missing role."
- **Answer:** The vague task. *"Here's a support ticket. What do you think?"* produced advice essays: **2% of replies could be read as labels, 0% were right**, at 362 output tokens each. The fixed prompt: **100% usable, 90% right, 30 tokens**. Second place: a broken example, at **25% valid JSON**.
- **Follow-up:** Isn't a vague task a beginner mistake nobody ships?
- **Follow-up answer:** The shipped version is subtler: a clear task with no definitions (build #009 measured that at 13-19%). Same problem: the model fills the gaps with its own idea of what you want.
- Notebook: [§2](notebook.ipynb#2-vague-task)

### ⭐ 2. Your format example used single quotes and a trailing comma. Does it matter if the instruction says "JSON"? · Mid
- **Trap:** "No. The model knows what JSON is."
- **Answer:** It copied the example. With `{'category': 'billing', …,}` as the example, only **25% of replies were valid JSON**; the first reply came back exactly in that broken style. The same prompt with a valid example: **100%**. The example beat the instruction.
- **Follow-up:** How do you stop that happening?
- **Follow-up answer:** Generate examples with code (`json.dumps`) instead of typing them, test that every example in a prompt parses, or use structured outputs (build #004) so the shape doesn't depend on the example at all.
- Notebook: [§6](notebook.ipynb#6-a-broken-format-example)

### 3. Does writing IMPORTANT in capitals make the model follow the rule? · Mid
- **Trap:** "Yes. That's why everyone does it."
- **Answer:** Not measurably. The calm line was already followed **100%** of the time, and so was the shouted one. Accuracy was **85% shouted vs 90% calm**, a 3-run difference out of 60, within noise.
- **Follow-up:** So is shouting harmless?
- **Follow-up answer:** On this task, it bought nothing. If a rule isn't followed, the cause is usually a conflict or a missing definition (anti-patterns 1, 2 and 5), and capitals don't fix either.
- Notebook: [§4](notebook.ipynb#4-shouting)

### 4. The system prompt says "under 50 words", the request says "in detail". What happens? · Mid
- **Trap:** "The system prompt wins."
- **Answer:** It splits the difference. With the conflict, **67%** of replies were under 50 words (longest 83). With one consistent instruction, **82%** (longest 56). Neither instruction fully won.
- **Follow-up:** The fix still missed 18% of the time. Why?
- **Follow-up answer:** Models count words loosely. If the limit matters, enforce it in code (count, then retry or truncate), as build #013 checked every rule in code.
- Notebook: [§3](notebook.ipynb#3-conflicting-instructions)

### 5. Is "Don't use markdown" a bad instruction? · Mid
- **Trap:** "Yes. Never tell a model what not to do."
- **Answer:** Not as bad as its reputation, here. With no instruction, **20%** of replies used markdown; "Don't use markdown" brought it to **5%**; saying what to do instead (*"one or two plain paragraphs, the way you'd type a plain-text email"*) brought it to **0%**.
- **Follow-up:** Then why prefer the positive version?
- **Follow-up answer:** It was better here (0% vs 5%) and it describes the target, so the model doesn't have to guess what "not markdown" should look like. But the negative version wasn't useless, and the data says so.
- Notebook: [§5](notebook.ipynb#5-only-saying-what-not-to-do)

### 6. You pasted 10,000 tokens of "context, just in case". Did accuracy drop? · Senior
- **Trap:** "Yes, the model gets distracted."
- **Answer:** Not here: **90% with or without it**. What changed was the bill: **10,983 vs 698 input tokens**, **$1.113 vs $0.085 per 1,000 tickets**, 13× the cost for nothing.
- **Follow-up:** Would prompt caching fix it?
- **Follow-up answer:** It would make the waste cheaper (build #006: reads cost a tenth), but the best fix is not sending it. Every token you send is a token you pay for, cache or not.
- Notebook: [§7](notebook.ipynb#7-padding-the-prompt-with-unrelated-context)

### 7. You ask the model for a 0-100 confidence and auto-accept anything above 90. Safe? · Senior
- **Trap:** "Yes, the model knows when it's unsure."
- **Answer:** Partly, and coarsely. Right answers averaged **88.5**, wrong ones **82.5**. In this run, **none of the 6 wrong answers scored 90 or above**, but only **18 of the 50 right answers** did, so the threshold would auto-accept about a third of tickets. The scores bunched between 70 and 97, and **4 of the 60 replies** didn't return a usable confidence at all.
- **Follow-up:** Would you ship it?
- **Follow-up answer:** Not on 56 data points. 6 wrong answers can't show that the threshold is safe. Check calibration on a much larger labelled set, keep a human on everything below the line, and re-check it whenever the prompt or model changes.
- Notebook: [§8](notebook.ipynb#8-trusting-the-models-confidence-score)

### 8. Of the 7, which would you fix first in a real codebase? · Senior
- **Trap:** "Whichever is easiest."
- **Answer:** The ones that changed results most here: vague tasks (0% → 90%) and broken examples (25% → 100% valid). Then context padding, which didn't hurt accuracy but cost 13×. Shouting and negative-only instructions mattered little on this task.
- **Follow-up:** How do you find them in an existing codebase?
- **Follow-up answer:** Run every prompt through the eval from build #014 and the tests from #015. The measurements tell you which habits actually cost you, which is what this notebook did.
- Notebook: [§9](notebook.ipynb#9-scorecard)
