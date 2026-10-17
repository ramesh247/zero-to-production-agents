# 06 · Stop guessing: improve prompts with a tiny eval set

Builds #009-#013 improved one prompt by looking at its mistakes. This notebook makes that loop explicit: three sets of 20 tickets with different jobs, four prompt versions (one deliberately overfitted), a 20-line eval harness, bootstrap ranges and ticket-by-ticket diffs.

**What you'll learn**
- Why a prompt that scored **85%** on its own examples scored **70%** on new tickets
- How a prompt reached **100%** on dev with rules aimed at single tickets, and why that proved nothing
- Which differences 20 tickets can detect (a 20-point gain) and which they can't (5 points)

## Quickstart
Needs an Anthropic API key. A full run (720 calls) costs about **6 cents** on Claude Haiku 5.5.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/02-prompt-engineering/06-eval-driven-prompting
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
cp .env.example .env        # then paste your key
jupyter notebook notebook.ipynb
```

## Results from a real run (Claude Haiku 5.5, thinking off, 3 runs per ticket)

All 3 labels right:

| Version | Dev (tuned on) | Validation | **Test** (labelled before any run) | Test, 95% range |
|---|---|---|---|---|
| v1: build #009's rubric | 85% | 73% | **70%** | 50-90% |
| v2: + 3 tie-breaks (build #010) | 87% | 87% | **85%** | 70-100% |
| v3: + 2 general rules from validation misses | 90% | 98% | **90%** | 75-100% |
| v4: + 4 rules aimed at specific dev tickets | **100%** | 93% | **95%** | 85-100% |

- **v1 → v3:** +20 points on test, 5 tickets better and 1 worse.
- **v4 looks perfect on dev,** drops on validation, and its +5 on test is one ticket none of its new rules mention. Ranges overlap with v3's.
- **Boundary tickets flip with any edit:** two tickets changed priority between low and medium across the versions, with all 3 runs agreeing inside each version.

## Files
- `notebook.ipynb`: the walkthrough and the eval harness, committed with outputs
- `data/tickets.json`: dev, validation and the 20 new test tickets, with labels
- `findings.json`: the numbers above plus every call, written by the last cell
- `.env.example`: copy to `.env` and add your key (`.env` is git-ignored)
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups

**Builds on:** [05 · Prompt chaining](../05-prompt-chaining/), and the prompts from [01](../01-anatomy-of-a-prompt/) and [02](../02-zero-vs-few-shot/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. Next: [07 · Versioning and testing prompts like code](../README.md).
