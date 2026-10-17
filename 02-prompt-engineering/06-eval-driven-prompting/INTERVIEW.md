# Interview pack: improving prompts with a tiny eval set

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb), run on **Claude Haiku 5.5** with thinking off.
Four versions of the ticket-triage prompt, scored on three sets of 20 tickets, 3 runs per ticket ("all 3 labels right"):

| Version | Dev (tuned on) | Validation | Test (labelled before any run) | Test, 95% range |
|---|---|---|---|---|
| v1 (build #009's rubric) | 85% | 73% | 70% | 50-90% |
| v2 (+ 3 tie-breaks, #010) | 87% | 87% | 85% | 70-100% |
| v3 (+ 2 rules from validation misses) | 90% | 98% | 90% | 75-100% |
| v4 (+ 4 rules aimed at specific dev tickets) | 100% | 93% | 95% | 85-100% |

---

### 1. Your prompt scores 85% on the tickets you built it with. What's its real accuracy? · Junior
- **Trap:** "85%. That's what the eval says."
- **Answer:** Lower. Build #009's prompt (v1) scored **85% on dev** (the tickets its rubric was written from), **73% on validation** and **70% on 20 new test tickets**: a 15-point gap. The dev number measures how well it fits the examples you looked at.
- **Follow-up:** How many tickets do you need in the test set?
- **Follow-up answer:** More than 20 for small differences: here one ticket moves the score 5 points, and the 95% range for v1's test score was 50-90%. 20 is enough to catch a 15-20 point problem, not to rank close versions.
- Notebook: [§4](notebook.ipynb#4-scores-by-version-and-set)

### ⭐ 2. Your new prompt scores 100% on dev. Do you ship it? · Mid
- **Trap:** "Yes. 100% is as good as it gets."
- **Answer:** Not on that evidence. v4 added four rules written for the exact dev tickets v1 missed ("requests for webhooks are positive"), and dev went to **100%**. On validation it **dropped from 98% to 93%**. On test it went from 90% to 95%, but that gain is one ticket none of the new rules mention, and the 95% ranges (**75-100% vs 85-100%**) overlap almost completely.
- **Follow-up:** So what would you ship?
- **Follow-up answer:** v3: 90% on test, built from general rules ("a login problem is account even when a bug causes it") rather than rules aimed at single tickets. Rules that name one ticket's wording can only help that ticket.
- Notebook: [§4](notebook.ipynb#4-scores-by-version-and-set), [§5](notebook.ipynb#5-how-much-is-noise)

### 3. v3 beats v2 by 5 points on test. Is v3 better? · Mid
- **Trap:** "Yes, 90 beats 85."
- **Answer:** The eval can't say. Ticket by ticket, v2 → v3 made **2 test tickets better and 1 worse** (net +3 runs out of 60). The 95% ranges are 70-100% and 75-100%. What it *can* say: v1 → v3 is a real change, **70% → 90%** on tickets nobody tuned on, with 5 better and 1 worse across the two steps.
- **Follow-up:** Then why keep v3?
- **Follow-up answer:** Because its two rules fixed specific, understood failures on validation (98% there), they're general, and they didn't make test worse. "Not proven better" isn't the same as "worse", but it should stop you announcing a 5-point win.
- Notebook: [§6](notebook.ipynb#6-ticket-by-ticket-what-each-version-fixed-and-broke)

### 4. Why do you need three sets? Isn't a train/test split enough? · Mid
- **Trap:** "Two is enough: tune on one, test on the other."
- **Answer:** Because you look at the second one too. v3's two new rules came from validation misses, and v3 scored **98% on validation** but **90% on test**. The moment you fix things you saw in a set, that set flatters you. The test set is the one you only score, never read.
- **Follow-up:** You looked at the hard test tickets in §6. What now?
- **Follow-up answer:** Then a v5 built from them can't be scored on this test set. Write a fresh test set before tuning again, and keep the old one as a regression set.
- Notebook: [§1](notebook.ipynb#1-three-sets-with-three-jobs)

### 5. A ticket keeps flipping between versions, even when you didn't touch its rule. Why? · Senior
- **Trap:** "The model is random."
- **Answer:** Within a version it isn't: all 3 runs agreed. But *"Would love a way to schedule reports to arrive every Monday"* went **medium, low, medium, low** across v1-v4, and *"Can I change the delivery address before it ships?"* went **medium, low, low, medium**. Both sit on a rule boundary ("someday idea" = low vs "a feature they'd use right away" = medium; "question" = low vs "simple fix" = medium), so any edit anywhere in the prompt tips them.
- **Follow-up:** How do you stop that?
- **Follow-up answer:** Make the boundary explicit for that pattern, or accept the ambiguity and don't count those tickets as signal. Either way, find them: they make every prompt change look like it did something.
- Notebook: [§6](notebook.ipynb#6-ticket-by-ticket-what-each-version-fixed-and-broke)

### 6. Running the eval takes time and money. How often should you run it? · Senior
- **Trap:** "Before each release."
- **Answer:** On every prompt change. All four versions on all three sets, 3 runs each, was **720 calls for $0.059**. That's cheaper than the time it takes to argue about whether a change helped.
- **Follow-up:** How do you make that automatic?
- **Follow-up answer:** Treat prompts like code: version them, run the eval in CI, and fail the build if the test score drops. That's build #015.
- Notebook: [§3](notebook.ipynb#3-the-eval-harness)

### 7. One test ticket was wrong in every version. What do you learn from it? · Senior
- **Trap:** "The model can't handle it. Use a bigger one."
- **Answer:** Look at the label first. *"The invoice PDF shows last year's address. Our finance team needs it fixed before month-end close tomorrow."* was wrong in all 4 versions: v1-v3 called it **billing**, and every version called the calm-but-urgent tone **neutral**, where my label says bug and negative. An invoice problem reads as billing. A ticket every version misses is either a gap in the rules or a label worth re-checking, and you can't tell which from the score.
- **Follow-up:** How do you decide?
- **Follow-up answer:** Read what the model answered, ask a colleague to label it blind, and only then change the rubric or the label. Never both at once, or you'll lose track of which one moved the score.
- Notebook: [§6](notebook.ipynb#6-ticket-by-ticket-what-each-version-fixed-and-broke)

### 8. What is the smallest eval that's still useful? · Senior
- **Trap:** "You need thousands of labelled examples."
- **Answer:** Small enough to start today. Three sets of 20 tickets caught a **15-point dev-to-test gap** (v1), showed a **20-point real improvement** (v1 → v3), and exposed a **100% dev score** that didn't hold up. What it can't do is rank versions 5 points apart.
- **Follow-up:** What's the next step up?
- **Follow-up answer:** Grow the test set from real traffic (especially the tickets that cause escalations), keep 3 runs per ticket, and report changes ticket by ticket, not just the average.
- Notebook: [§5](notebook.ipynb#5-how-much-is-noise)
