# 01 · Anatomy of a production prompt: role, context, task, format

Every prompt guide lists the same four parts. This notebook measures what each one is worth on a real job, triaging support tickets, by adding them one at a time and then removing each from the full prompt.

**What you'll learn**
- Why the output **format** took usable replies from 25% to 100%, and cut output tokens from 178 to 29
- Why **context** (your team's definitions) was worth +30 points, and still +33 on tickets it was never tuned on
- Why the **role** ("You are a support triage lead…") moved the score by 1 run out of 60

## Quickstart
Needs an Anthropic API key. A full run (576 calls) costs about **4 cents** on Claude Haiku 5.5.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/02-prompt-engineering/01-anatomy-of-a-prompt
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
cp .env.example .env        # then paste your key
jupyter notebook notebook.ipynb
```

## Results from a real run (Claude Haiku 5.5, thinking off, 3 runs per prompt)

"All 3 right" = category, priority and sentiment all match my labels. **Dev** = the 20 tickets from build #004 (the rubric was written from them). **Test** = 12 new tickets, labelled with the rubric before any model run.

| Prompt | Dev: all 3 right | Test: all 3 right | Usable replies (dev / test) | Output tokens (dev) | $ per 1,000 tickets (dev) |
|---|---|---|---|---|---|
| A: task only | 13% | 19% | 25% / 33% | 178 | $0.097 |
| B: + format | 55% | 42% | 100% / 100% | 29 | $0.031 |
| C: + context | 85% | 75% | 100% / 100% | 29 | $0.067 |
| **D: + role (full prompt)** | **87%** | **75%** | 100% / 100% | 29 | $0.071 |
| D without context | 68% | 47% | 100% / 100% | 29 | $0.035 |
| D without format | 50% | 67% | 57% / 75% | 117 | $0.106 |

**One ticket:** *"Hi, I was charged twice for order ORD-48213. Please refund the extra $49.99."*
- Task only: a markdown essay ending "Priority: Medium… Sentiment: Neutral to mildly negative" (unusable).
- \+ format: `{"category": "billing", "priority": "medium", "sentiment": "neutral"}`
- \+ context: `{"category": "billing", "priority": "high", "sentiment": "neutral"}`, which matches the rubric's "charged twice for the same order = high".

## Files
- `notebook.ipynb`: the walkthrough, committed with its outputs
- `data/tickets.json`: the dev and test tickets with labels
- `findings.json`: the numbers above plus every call, written by the last cell
- `.env.example`: copy to `.env` and add your key (`.env` is git-ignored)
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups

**Builds on:** the tickets from [04 · Reliable JSON](../../01-genai-llm-foundations/04-structured-outputs/) and the model choice from [08 · Choosing a model](../../01-genai-llm-foundations/08-choosing-a-model/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. Next: [02 · Zero-shot vs few-shot](../02-zero-vs-few-shot/).
