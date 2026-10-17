# 03 · Chain-of-thought and extended thinking, measured

"Think step by step" in the prompt vs the model's built-in extended thinking at three effort levels, on a task that needs reasoning (counting across a 150-product catalog) and one that doesn't (ticket triage). What each costs in tokens, seconds and dollars.

**What you'll learn**
- Why "think step by step" scored **73%** on counting questions, the same as "answer only", while built-in thinking scored **100%**
- Why thinking cost about the same as no thinking on hard questions, and twice as much on easy ones
- Why reasoning made ticket triage slightly **worse** (87% → 83%)

## Quickstart
Needs an Anthropic API key. A full run (480 calls) costs about **20 cents** on Claude Haiku 5.5; the catalog is prompt-cached.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/02-prompt-engineering/03-chain-of-thought
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
cp .env.example .env        # then paste your key
jupyter notebook notebook.ipynb
```

## Results from a real run (Claude Haiku 5.5, 3 runs per question)

**Task A: 20 catalog questions** (16 counting, 4 lookups):

| Setting | Counting questions | Lookups | Avg output tokens | Median s | $ per 1,000 questions |
|---|---|---|---|---|---|
| Answer only (thinking off) | 73% | 100% | 877 | 2.52 | $0.567 |
| "Think step by step" (thinking off) | 73% | 100% | 1,069 | 3.08 | $0.645 |
| Thinking, effort low | 96% | 100% | 956 | 2.79 | $0.607 |
| **Thinking, effort medium (default)** | **100%** | 100% | 1,050 | 3.51 | $0.634 |
| Thinking, effort high | 100% | 100% | 1,166 | 3.49 | $0.692 |

With thinking off, the "answer only" prompt still wrote ~1,100 tokens of visible working on counting questions (12 on lookups), so it was effectively chain-of-thought too.

**Task B: ticket triage** (build #010's 20 fresh tickets, rubric v2):

| Setting | All 3 labels right | Median s | $ per 1,000 tickets |
|---|---|---|---|
| **Answer only** | **87%** | 0.73 | $0.084 |
| "Think step by step" | 83% | 1.50 | $0.170 |
| Thinking, effort medium | 83% | 1.11 | $0.136 |

## Files
- `notebook.ipynb`: the walkthrough, committed with its outputs
- `data/tickets.json`: build #010's fresh tickets with labels
- `findings.json`: the numbers above plus every call, written by the last cell
- `.env.example`: copy to `.env` and add your key (`.env` is git-ignored)
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups

**Builds on:** [02 · Zero-shot vs few-shot](../02-zero-vs-few-shot/), the catalog from [06 · Prompt caching](../../01-genai-llm-foundations/06-prompt-caching/) and [08 · Choosing a model](../../01-genai-llm-foundations/08-choosing-a-model/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. Next: [04 · XML tags and output templates](../04-xml-and-output-formatting/).
