# Interview pack: prompt chaining

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb), run on **Claude Haiku 5.5** with thinking off.
The job: for each of 40 support tickets (builds #004 and #010), label it (rubric v2), extract the order id and whether
the customer asks for money back, and write a reply that follows 5 policy rules a program can check. 3 runs each.

| Design | Labels right | Fields right | Reply follows all 5 rules | Everything right | Calls | Median s per ticket | $ per 1,000 tickets |
|---|---|---|---|---|---|---|---|
| One prompt | 77% | 100% | 97% | 73% | 1 | 1.42 | $0.200 |
| Chain, code picks the rules | 80% | 100% | 93% | 74% | 3 | 2.88 | $0.232 |
| Chain, all rules | 82% | 100% | 74% | 57% | 3 | 2.88 | $0.246 |

---

### 1. Is a chain of small prompts always better than one big prompt? · Junior
- **Trap:** "Yes. Smaller tasks, fewer mistakes."
- **Answer:** Not here. One prompt got **73%** of tickets completely right; the best chain got **74%**, while taking **twice as long** (2.88 s vs 1.42 s median per ticket) and costing more ($0.232 vs $0.200 per 1,000). This "hard" prompt wasn't hard enough for the model to need splitting.
- **Follow-up:** When would you expect chaining to win?
- **Follow-up answer:** When one prompt measurably fails: very long inputs, steps that need different settings (thinking on for one, off for another), or a step that needs a tool or a lookup in between. Measure the one-prompt version first.
- Notebook: [§3](notebook.ipynb#3-run-them)

### ⭐ 2. You split the prompt into three steps and the replies got worse. How? · Mid
- **Trap:** "Information got lost between the steps."
- **Answer:** The opposite: the last step got more to interpret. In "chain, all rules", the reply step received the whole policy plus "priority high" and had to decide which rules applied. It said the ticket was **escalated on 22 replies to high-priority tickets**, where the policy says escalate only urgent ones, and it wrote "high-priority issue" into replies. Reply compliance fell to **74%**. When **code** picked the rules from steps 1-2 ("say refunds take 5-7 business days", "don't say it was escalated"), escalation was correct in **100%** of replies.
- **Follow-up:** So what was the chain actually for?
- **Follow-up answer:** Moving decisions out of the model and into code. Splitting alone made things worse; splitting so that code can turn intermediate answers into explicit rules is what helped.
- Notebook: [§4](notebook.ipynb#4-which-policy-rules-broke)

### 3. Did splitting improve the labels? · Mid
- **Trap:** "A lot. The label step has one job."
- **Answer:** A little: **77%** in the one prompt, **80-82%** as a dedicated step. That's 96-98 vs 92 correct out of 120 runs. Small, and the one-prompt version still finished the whole job in half the time.
- **Follow-up:** Would you chain just for that?
- **Follow-up answer:** Only if label accuracy is what you're paid for. A cheaper first move is improving the rubric (build #010), which helps both designs.
- Notebook: [§3](notebook.ipynb#3-run-them)

### 4. Every design "failed" the refund rule on the same ticket. Why? · Mid
- **Trap:** "That ticket is just hard."
- **Answer:** The checker was wrong, not the model. Ticket 8 is in Spanish, and every design replied in Spanish: *"Los reembolsos tardan entre 5 y 7 días hábiles"*. My check looks for the English phrase "5-7 business days", so all 9 replies counted as misses. Those are the only refund-rule misses in the whole run.
- **Follow-up:** What does that teach you about rule-based checks?
- **Follow-up answer:** Read the failures before trusting the number. A check that encodes one language, one phrasing or one format silently fails on everything else. Fix the check (or label the case), then re-score.
- Notebook: [§4](notebook.ipynb#4-which-policy-rules-broke)

### 5. Is "never mention the priority" a good rule to check with a regex? · Senior
- **Trap:** "Yes, just search for the word."
- **Answer:** Half-good. It caught a real leak: the all-rules chain wrote *"Since this is a high-priority issue, we've escalated it"*. It also flagged ordinary English: *"we've passed it to engineering as a priority"*. One prompt had 1 flag, code-picked rules 2, all-rules chain 7.
- **Follow-up:** How would you check it better?
- **Follow-up answer:** Look for the label values in label positions ("high-priority", "priority: high") rather than the word alone, and keep a small list of hand-checked replies to test the checker itself.
- Notebook: [§4](notebook.ipynb#4-which-policy-rules-broke)

### 6. Your chain is 3 calls. Where does the latency go? · Senior
- **Trap:** "3 calls means 3× the time."
- **Answer:** About 2×: **2.88 s vs 1.42 s** median per ticket. The label and field steps are short (structured output, no reply to write), so the chain costs roughly two extra short calls, not two extra full ones.
- **Follow-up:** How would you cut it?
- **Follow-up answer:** Run steps 1 and 2 in parallel, since neither needs the other's output. Only the reply waits for both. I didn't measure that here.
- Notebook: [§3](notebook.ipynb#3-run-them)

### 7. Fields were 100% right in every design. What does that tell you? · Senior
- **Trap:** "Extraction is solved."
- **Answer:** That these fields were easy: order ids like "ORD-48213" and an explicit "refund" request, 120 out of 120 runs in all three designs. It doesn't tell you about messier fields (amounts in words, "the order from last Tuesday").
- **Follow-up:** Would you still keep extraction as its own step?
- **Follow-up answer:** Yes if code needs it (to look up the order before replying), since a separate structured step is easy to test and log. Otherwise the one prompt already got it right.
- Notebook: [§3](notebook.ipynb#3-run-them)

### 8. When does a chain earn its extra calls? · Senior
- **Trap:** "Whenever the task has more than one part."
- **Answer:** When something needs to happen between the steps. Here, the only design that matched one prompt was the one where **code** read the labels and fields and chose the reply rules. Splitting without that made it worse (57% everything right).
- **Follow-up:** Give an example where the chain clearly wins.
- **Follow-up answer:** When step 2's output drives a real lookup: fetch the order, check it was paid, then tell the reply step the actual refund amount. One prompt can't do that; the chain plus code can. That's the agents subject coming up in this series.
- Notebook: [§2](notebook.ipynb#2-three-designs)
