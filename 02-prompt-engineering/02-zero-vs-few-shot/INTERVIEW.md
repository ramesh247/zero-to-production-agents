# Interview pack: zero-shot vs few-shot

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb), run on **Claude Haiku 5.5** with thinking off.
Same task as build #009 (label support tickets with category, priority and sentiment). Eight prompts, 3 runs each.
Examples come only from the 20 dev tickets. The main score is on **20 fresh tickets**, labelled before any model run.
"All 3 right" means all three labels matched mine.

| Prompt (fresh set) | All 3 right | $ per 1,000 tickets | Input tokens |
|---|---|---|---|
| No rubric, no examples | 42% (25/60) | $0.034 | 199 |
| No rubric, 8 examples | 60% (36/60) | $0.105 | 906 |
| Rubric v1 (#009 prompt), no examples | 78% (47/60) | $0.070 | 557 |
| Rubric v1 + 2 examples | 82% (49/60) | $0.091 | 760 |
| Rubric v1 + 4 examples | 85% (51/60) | $0.108 | 930 |
| Rubric v1 + 8 examples | 80% (48/60) | $0.141 | 1,264 |
| Rubric v1 + 4 examples, all priority "high" | 80% (48/60) | $0.107 | 921 |
| Rubric v2 (3 tie-break lines), no examples | 85% (51/60) | $0.080 | 651 |

---

### 1. More examples, better results? · Junior
- **Trap:** "Yes. 8 examples beat 4, 4 beat 2."
- **Answer:** Not here. With the rubric in place: **2 examples 82%, 4 examples 85%, 8 examples 80%**, while the cost per 1,000 tickets doubled from $0.070 (no examples) to $0.141 (8). The 8-example set wasn't better than the 4-example set it contains.
- **Follow-up:** How do you pick how many?
- **Follow-up answer:** Measure on held-out data and stop where it flattens. Here that's 2-4. Every example is paid on every call, so extras that don't move the score are pure cost.
- Notebook: [§3](notebook.ipynb#3-run-them)

### ⭐ 2. Your prompt misses edge cases. Add examples or fix the rules? · Mid
- **Trap:** "Add examples. That's what few-shot is for."
- **Answer:** Fixing the rules matched the best few-shot prompt for less. Three tie-break lines (rubric v2) scored **85% (51/60)**, the same as 4 examples, at **$0.080 vs $0.108 per 1,000** tickets: 94 extra input tokens instead of 373. The misses in build #009 were rule conflicts, and a rule fixes a conflict once, for every ticket like it.
- **Follow-up:** Was the rule fix free?
- **Follow-up answer:** No. It fixed two fresh tickets but broke one: see question 5.
- Notebook: [§4](notebook.ipynb#4-do-examples-replace-a-rubric)

### 3. Can you skip writing the rules and just show examples? · Mid
- **Trap:** "Yes. Examples show what you mean better than definitions."
- **Answer:** They helped, but didn't replace the rules. Without a rubric, 8 examples lifted "all 3 right" from **42% to 60%**. The rubric alone, with no examples, scored **78%** at a lower cost ($0.070 vs $0.105 per 1,000).
- **Follow-up:** When would examples alone be enough?
- **Follow-up answer:** When the categories are obvious and the boundaries don't matter much. Here, priority is a team decision ("charged twice = high"), and 8 examples can't cover every boundary a written rule can state.
- Notebook: [§4](notebook.ipynb#4-do-examples-replace-a-rubric)

### 4. All 4 of your examples are labelled "high". Does the model start saying "high" for everything? · Mid
- **Trap:** "Yes. Few-shot examples bias the label distribution."
- **Answer:** Not in this run. On the fresh tickets whose label isn't "high", the skewed prompt said "high" **0 times in 45 runs**, the same as the balanced prompts, and its predicted priority counts were identical to the no-example prompt. With a written rubric, the definitions won.
- **Follow-up:** Would you rely on that?
- **Follow-up answer:** No. I only tested skew with the rubric present. Without definitions the model leans on examples more (they were worth +18 points there), so skew could matter. Keep examples balanced; it costs nothing.
- Notebook: [§5](notebook.ipynb#5-skewed-examples-all-high)

### 5. A rule fix made a ticket that used to pass fail. How? · Senior
- **Trap:** "Bad luck, the model is random."
- **Answer:** The new rule spread further than intended. "A bug the customer calls minor is still negative" fixed *"Small issue"* (neutral → negative, as labelled), but *"Wrong colour. Not a big deal, an exchange would be fine"* went from neutral (correct) to **negative on all 3 runs**. That ticket is a shipping mistake, not a bug, but the model applied the "minor still means negative" idea anyway.
- **Follow-up:** How do you catch side-effects like this?
- **Follow-up answer:** Re-run the whole held-out set after every rule change, not just the tickets you meant to fix, and compare ticket by ticket. Here v2 fixed 2 tickets and broke 1: net +4 runs out of 60.
- Notebook: [§4](notebook.ipynb#4-do-examples-replace-a-rubric)

### 6. One ticket was wrong in every single prompt. Whose fault? · Senior
- **Trap:** "The model's. It's a weak model."
- **Answer:** Probably mine. *"Thanks for the quick refund, appreciated!"* came back as **billing in 24 out of 24 runs** across all 8 prompts. My rubric says praise is feature_request, but it also says refunds are billing. When every prompt makes the same "mistake", check the label.
- **Follow-up:** What do you do with it?
- **Follow-up answer:** Make a decision and write it down: "thanks about a specific transaction is billing" or "all praise is feature_request". Either is fine; having both rules in the rubric isn't.
- Notebook: [§4](notebook.ipynb#4-do-examples-replace-a-rubric)

### 7. 85% vs 78%. Is the improvement real? · Senior
- **Trap:** "7 points is a clear win."
- **Answer:** It's **51 vs 47 correct runs out of 60**, from a handful of tickets. That's a real but small difference, and one rule change moved tickets in both directions. The large, unambiguous gap in this notebook is **rubric vs no rubric: 78% vs 42%**.
- **Follow-up:** What would make you confident?
- **Follow-up answer:** More fresh tickets (especially the hard ones), the same 3 runs, and reporting the tickets that changed, not just the average. That's build #014.
- Notebook: [§3](notebook.ipynb#3-run-them)

### 8. Rubric v2 scored 100% on build #009's test set. Why isn't that the headline? · Senior
- **Trap:** "Because 100% sounds too good to be true."
- **Answer:** Because it isn't a fair test. I wrote v2's tie-breaks after seeing #009's 3 misses, so that set is no longer held out. On the 20 fresh tickets labelled before this run, v2 scored **85%**. Reporting the 100% would be grading on the answer key.
- **Follow-up:** Do you throw the old test set away?
- **Follow-up answer:** Keep it as a regression set, so old fixes don't break again, but never quote it as accuracy for a prompt that was tuned on it. Each round of tuning needs fresh held-out data.
- Notebook: [§1](notebook.ipynb#1-data-examples-from-dev-scores-on-fresh-tickets)
