# 05 · Prompt chaining: break one hard prompt into three easy ones

Label a support ticket, extract its order details and write a reply that follows 5 policy rules: as one prompt, and as a 3-step chain. Every output is checked by code. The surprise: splitting alone didn't help; letting code choose the rules between steps did.

**What you'll learn**
- Why one prompt (**73%** completely right, 1.42 s) matched the best chain (**74%**, 2.88 s)
- How a naive chain made replies **worse** (97% → 74% rule-compliant), escalating high-priority tickets 22 times
- Why the checker, not the model, "failed" every reply to a Spanish ticket

## Quickstart
Needs an Anthropic API key. A full run costs about **8 cents** on Claude Haiku 5.5.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/02-prompt-engineering/05-prompt-chaining
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
cp .env.example .env        # then paste your key
jupyter notebook notebook.ipynb
```

## Results from a real run (Claude Haiku 5.5, thinking off, 40 tickets × 3 runs)

| Design | Labels right | Fields right | Reply follows all 5 rules | Everything right | Median s per ticket | $ per 1,000 tickets |
|---|---|---|---|---|---|---|
| **One prompt** | 77% | 100% | **97%** | 73% | **1.42** | **$0.200** |
| Chain, code picks the rules | 80% | 100% | 93% | **74%** | 2.88 | $0.232 |
| Chain, all rules | 82% | 100% | 74% | 57% | 2.88 | $0.246 |

- **Why "chain, all rules" broke:** the reply step got the whole policy plus "priority high" and escalated **22 replies to high-priority tickets** (policy: urgent only). It also wrote "high-priority issue" into replies.
- **Checker limits:** all 9 refund-rule "misses" are ticket 8, which is in Spanish; every design correctly replied "entre 5 y 7 días hábiles". The "no internal labels" check also flags everyday phrases like "as a priority".

## Files
- `notebook.ipynb`: the walkthrough, committed with its outputs
- `data/tickets.json`: the 40 tickets with labels, order ids and refund flags
- `findings.json`: the numbers above plus every reply, written by the last cell
- `.env.example`: copy to `.env` and add your key (`.env` is git-ignored)
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups

**Builds on:** [03 · Chain-of-thought](../03-chain-of-thought/) and [04 · XML tags and output templates](../04-xml-and-output-formatting/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. Next: [06 · Eval-driven prompting](../README.md).
