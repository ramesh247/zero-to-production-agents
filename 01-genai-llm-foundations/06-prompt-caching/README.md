# 06 · Prompt caching: cut latency and cost on repeated context

A support assistant with a big, stable system prompt (a 150-product catalog and its policies) answers 10 questions, with and without prompt caching, on Claude Haiku 4.5. Then it breaks caching on purpose, the two ways it fails silently in real apps.

**What you'll learn**
- Why caching cut input cost by **78%**, not the 90% the price list suggests
- Why a prompt under **4,096 tokens** doesn't cache at all, with no error
- How one timestamp in the system prompt made caching cost **25% more** than not caching
- When caching makes responses faster, and when it doesn't

## Quickstart
Needs an Anthropic API key. A full run costs roughly **$0.50** on Claude Haiku 4.5 (most of it is the 52K-token latency test).
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/01-genai-llm-foundations/06-prompt-caching
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
cp .env.example .env        # then paste your key
jupyter notebook notebook.ipynb
```

## Results from a real run (Claude Haiku 4.5)

**Same 7,928-token system prompt, same 10 questions:**

| Setup | Full-price input | Cache write | Cache read | Input cost | Total cost |
|---|---|---|---|---|---|
| No caching | 79,378 | 0 | 0 | $0.0794 | $0.0836 |
| Cached (5-min TTL) | 168 | 7,921 | 71,289 | **$0.0172 (−78%)** | $0.0216 (−74%) |

**Silent failure #1:** a **2,971-token** prompt marked for caching, sent 3 times: **0 written, 0 read**. Claude Haiku 4.5's minimum cacheable prefix is 4,096 tokens.

**Silent failure #2:** a timestamp at the top of the system prompt. Every call wrote a new cache, none read one. Input cost for 5 questions:

| No caching | Caching done right | Timestamp in the prompt |
|---|---|---|
| $0.0397 | **$0.0132** | $0.0497 (+25% vs no caching) |

**Latency** (median time to first text):

| Prompt size | No caching | Cache reads |
|---|---|---|
| 8K tokens | 0.444 s | 0.450 s |
| 52K tokens | 0.80 s | 0.56 s |

The 52K test is 5 calls each way and single uncached calls ranged from 0.43 s to 1.00 s, so read it as a direction, not a benchmark. Input cost for those 5 calls: **$0.261 → $0.086**.

## Files
- `notebook.ipynb`: the walkthrough, committed with its outputs
- `findings.json`: the numbers above, written by the last cell
- `.env.example`: copy to `.env` and add your key (`.env` is git-ignored)
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups

**Builds on:** [05 · Context windows and cost](../05-context-windows-and-cost/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. Next: [07 · Images and PDFs as input](../README.md).
