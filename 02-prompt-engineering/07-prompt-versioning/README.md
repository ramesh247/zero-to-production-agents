# 07 · Versioning and testing prompts like code

A small, working setup for treating prompts like code: one file per prompt version, a lock file of hashes, an eval command with **record / replay** snapshots, a pytest suite that runs offline in milliseconds, and a gate that fails CI when a new version scores worse than the released one.

**What you'll learn**
- How to run prompt tests in CI with **no API key, no cost, in 0.02 s**, and still catch every prompt change
- Why editing a released prompt in place should fail the build, and what the failure looks like
- How much a re-run of the *same* prompt moves the score, and why the gate compares against a replayed baseline

## Quickstart
The tests run without an API key (replay mode). Recording a new version needs a key and costs about half a cent.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/02-prompt-engineering/07-prompt-versioning
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q                                                    # replay: free, offline
python -m src.evaluate triage@v3 --set test --baseline triage@v2      # replay a comparison
cp .env.example .env                                                   # then paste your key, to record:
python -m src.evaluate triage@v4 --set test --mode record --baseline triage@v3 --max-drop 0.05
```

## Layout
```
prompts/triage/v1.md, v2.md, v3.md, v3.1.md   one file per version (front matter: description, system prompt)
prompts/lock.json                              hash of every released version
src/prompts.py                                 load "name@version", hash it, write the lock file
src/llm.py                                     call the model; record / replay snapshots keyed by model + prompt hash + ticket + run
src/evaluate.py                                score a version, compare with a baseline, gate (exit code 1 on failure)
tests/test_prompts.py                          lock file, golden tickets, score gate
snapshots/                                     recorded replies (300 of them)
ci/prompt-tests.yml                            example GitHub Actions workflow
results/demo.txt                               the full demo below, with real output
```

## Results from a real run (Claude Haiku 5.5, thinking off, build #014's 20 test tickets × 3 runs)

| Step | Output |
|---|---|
| Record v1 / v2 / v3 | 70% / 85% / 90% all 3 labels right, about $0.005 each |
| Replay v3 vs v2 | 90% vs 85%, tickets better: 2, worse: 1, **$0.0000, 0.00 s** |
| `pytest -q` | **8 passed in 0.02 s** |
| Gate: v1 vs released v3, max drop 5% | **GATE FAILED: dropped 20%**, exit code 1 |
| Re-run v3 live (same prompt) | 92%: one ticket flipped |
| Edit v3 in place ("When two rules disagree" → "If …") | **6 failed, 2 passed**: "triage@v3 was edited after release" |
| Release that edit as v3.1, record, compare | 90% vs 90%, 0 better, 0 worse, $0.0051 |

The whole demo, commands and output, is in [`results/demo.txt`](results/demo.txt). Total API cost to record everything: **$0.024**.

## Files
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups
- `findings.json`: the numbers above, parsed from `results/demo.txt`
- `data/tickets.json`: build #014's dev, validation and test tickets
- `.env.example`: copy to `.env` and add your key, only needed to record (`.env` is git-ignored)

**Builds on:** [06 · Eval-driven prompting](../06-eval-driven-prompting/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. Next: [08 · 7 prompt anti-patterns](../08-prompt-anti-patterns/).
