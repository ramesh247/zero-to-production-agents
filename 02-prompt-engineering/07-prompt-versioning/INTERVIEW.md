# Interview pack: versioning and testing prompts like code

Every answer is backed by the real run in [results/demo.txt](results/demo.txt) (numbers collected in [findings.json](findings.json)),
using **Claude Haiku 5.5** with thinking off on build #014's 20 test tickets, 3 runs per ticket.

| What | Result |
|---|---|
| Record v1 / v2 / v3 on the test set | 70% / 85% / 90% all 3 labels right, about $0.005 and 6-11 s each |
| Replay v3 from snapshots | 90%, $0.0000, 0.00 s |
| `pytest` (replay mode) | 8 passed in 0.02 s, no API key |
| Edit released v3 in place ("When" → "If") | 6 failed, 2 passed |
| Gate: v1 against released v3, max drop 5% | GATE FAILED: dropped 20%, exit code 1 |
| Same v3 prompt, run live again | 92% (one ticket flipped) |
| v3.1 = the "When" → "If" edit, released properly | 90%, 0 tickets better, 0 worse |

---

### 1. Why keep prompts in versioned files instead of strings in the code? · Junior
- **Trap:** "It's just tidier."
- **Answer:** So a prompt change becomes a reviewable, testable release. Each version is a file (`prompts/triage/v3.md`), its hash is locked in `prompts/lock.json`, and released versions are immutable. When I changed one word in the released v3, **6 of 8 tests failed** and the first message said exactly what happened: *"triage@v3 was edited after release … copy it to a new version file instead."*
- **Follow-up:** What about a tiny typo fix?
- **Follow-up answer:** Same rule. The model reads every byte, and build #014 showed that edits unrelated to a ticket's rule can still flip it. New version, record, compare.
- Code: [tests/test_prompts.py](tests/test_prompts.py)

### ⭐ 2. LLM tests are slow, cost money and give different answers each run. How do you test prompts in CI? · Mid
- **Trap:** "You can't. Test prompts by hand."
- **Answer:** Record once, replay in CI. Each reply is saved under a key of **model + prompt hash + ticket + run**. In CI the tests read those snapshots: **8 tests passed in 0.02 s, for $0, with no API key**. Recording all three versions on the test set cost **$0.014** (plus $0.005 for v3 on dev). Because the prompt hash is in the key, editing a prompt makes its snapshots disappear, so CI can't quietly test an old recording against a new prompt: it fails with *"MissingSnapshot … run the eval with --mode record"*.
- **Follow-up:** Doesn't replay just test that the past is unchanged?
- **Follow-up answer:** Yes, for unchanged prompts, and that's the point: those tests check the code around the prompt (parsing, gates, golden tickets). A *new* prompt version has no snapshots, so it must be recorded, which runs the real eval and the gate.
- Code: [src/llm.py](src/llm.py)

### 3. You re-ran the exact same prompt and got 92% instead of 90%. Which is right? · Mid
- **Trap:** "The higher one. Or average them."
- **Answer:** Both are real, and that's the noise you're working with. The live re-run of v3 got **55/60 vs the recorded 54/60**: one run of one ticket (the "schedule reports" ticket that build #014 found on a rule boundary) came out differently.
- **Follow-up:** So what does a gate compare against?
- **Follow-up answer:** The recorded baseline, replayed, not a fresh re-run of it. My first version of this demo re-ran the baseline too, and its score moved by itself. Then set the allowed drop above that noise.
- Results: [§5 in demo.txt](results/demo.txt)

### 4. You changed "When two rules disagree" to "If two rules disagree". Do you need to re-run the eval? · Mid
- **Trap:** "No, it's cosmetic."
- **Answer:** You can't know without running it, and running it is cheap. Released as v3.1, it scored **90%, with 0 tickets better and 0 worse** than v3, for **$0.0051**. This time nothing moved. In build #014, edits that didn't touch a ticket's rule did flip boundary tickets.
- **Follow-up:** How would you make cheap checks the default?
- **Follow-up answer:** Make the release path do it: new version file → record → compare with the baseline → gate. Nobody has to decide whether an edit is "big enough".
- Results: [§7 in demo.txt](results/demo.txt)

### 5. What should the gate check? · Senior
- **Trap:** "That accuracy is above some number."
- **Answer:** Two things: a floor (`--min-score`) and a maximum drop against the released version (`--max-drop`). Evaluating v1 against v3 with a 5% allowance printed *"GATE FAILED: dropped 20%"* and exited 1, which is what fails a CI job.
- **Follow-up:** How do you choose the allowed drop?
- **Follow-up answer:** Above the noise. Here one run is 1.7 points (1 of 60) and a same-prompt re-run moved 2 points, so 5% tolerates a couple of flips but catches a real regression. With a bigger test set you can tighten it.
- Code: [src/evaluate.py](src/evaluate.py)

### 6. You have a score gate. Why also test specific "golden" tickets? · Senior
- **Trap:** "The average already covers them."
- **Answer:** An average can stay flat while an important ticket breaks. The suite pins four tickets the team must never get wrong: a double charge is billing/high, *"YOUR CHECKOUT PAGE IS DOWN"* is bug/urgent, a hijacked account is account/urgent, and *"Charged three times!!"* is billing/high, on all 3 runs.
- **Follow-up:** Which tickets become golden?
- **Follow-up answer:** The ones where a wrong label costs real money or trust (security, outages, double charges), plus every past incident: when a ticket was mishandled in production, it goes in the list.
- Code: [tests/test_prompts.py](tests/test_prompts.py)

### 7. The provider releases a new model version. What happens to your tests? · Senior
- **Trap:** "Nothing. The prompts didn't change."
- **Answer:** The model id is part of the snapshot key, so changing `MODEL` invalidates every snapshot, and replay fails until you record again. That's on purpose: a model change is a change to every prompt at once. Checked by changing the model name in a copy of the repo: **5 failed, 4 passed** (the 4 lock-file tests don't depend on the model). Nothing was recorded on a real new model.
- **Follow-up:** How would you roll it out?
- **Follow-up answer:** Record every current prompt on the new model, compare each with its replayed baseline, and treat any gate failure as a prompt you need to re-tune for that model (build #008 showed models differ per task).
- Code: [src/llm.py](src/llm.py)

### 8. Why not just compare the new prompt with a fresh run of the old one? · Senior
- **Trap:** "That's the fairest comparison: same day, same conditions."
- **Answer:** It adds the old prompt's noise to the comparison. I hit this building the demo: comparing v3.1 with a freshly re-recorded v3 made v3 score 92% instead of its released 90%, so the comparison moved for reasons unrelated to the edit. Now the baseline is always replayed from its snapshots.
- **Follow-up:** When would you refresh a baseline recording?
- **Follow-up answer:** Only on purpose: a model change, a bigger test set, or a scheduled re-baseline with the result reviewed. Never as a side effect of testing something else.
- Code: [src/evaluate.py](src/evaluate.py)
