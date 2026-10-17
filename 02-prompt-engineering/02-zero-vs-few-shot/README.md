# 02 · Zero-shot vs few-shot: when examples actually help

Build #009's ticket-labelling prompt missed on edge cases. The usual advice is "add examples". This notebook tests 0, 2, 4 and 8 examples, examples without written rules, deliberately skewed examples, and the alternative: three tie-break lines added to the rules.

**What you'll learn**
- Why three tie-break rules matched the best few-shot prompt (**85%**) for a quarter of the extra tokens
- Why 8 examples scored lower than 4, at twice the cost of no examples
- Why examples without written rules reached only **60%**, against **78%** for the rules alone

## Quickstart
Needs an Anthropic API key. A full run (768 calls) costs about **7 cents** on Claude Haiku 5.5.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/02-prompt-engineering/02-zero-vs-few-shot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
cp .env.example .env        # then paste your key
jupyter notebook notebook.ipynb
```

## Results from a real run (Claude Haiku 5.5, thinking off, 3 runs per prompt)

Scored on **20 fresh tickets** labelled before any model run. Examples come only from the 20 dev tickets.

| Prompt | All 3 labels right | $ per 1,000 tickets |
|---|---|---|
| No rubric, no examples | 42% | $0.034 |
| No rubric, 8 examples | 60% | $0.105 |
| Rubric v1 (build #009), no examples | 78% | $0.070 |
| Rubric v1 + 2 / 4 / 8 examples | 82% / **85%** / 80% | $0.091 / $0.108 / $0.141 |
| Rubric v1 + 4 examples, all priority "high" | 80% (said "high" wrongly 0/45 times) | $0.107 |
| **Rubric v2: v1 + 3 tie-break lines, no examples** | **85%** | **$0.080** |

- **The rule fix wasn't free:** v2 fixed 2 fresh tickets and broke 1 ("wrong colour, not a big deal" became negative).
- **One ticket was wrong everywhere:** "Thanks for the quick refund" came back as billing in 24/24 runs. My rubric says praise is feature_request *and* refunds are billing, so that's a rule conflict, not a model failure.
- On build #009's 12 test tickets, v2 scored 36/36, but its tie-breaks were written after seeing those misses, so that set is no longer held out.

## Files
- `notebook.ipynb`: the walkthrough, committed with its outputs
- `data/tickets.json`: dev, build #009's test set, and the 20 fresh tickets, with labels
- `findings.json`: the numbers above plus every call, written by the last cell
- `.env.example`: copy to `.env` and add your key (`.env` is git-ignored)
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups

**Builds on:** [01 · Anatomy of a production prompt](../01-anatomy-of-a-prompt/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. Next: [03 · Chain-of-thought and extended thinking](../README.md).
