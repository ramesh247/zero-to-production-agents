# 04 · Getting reliable JSON out of an LLM

Extract 6 fields from 20 messy support tickets, three ways, and measure how often you get data your code can actually use: "Reply in JSON", the schema in the prompt (with a retry, or with the usual fence-stripping hack), and the API's structured outputs.

**What you'll learn**
- Why "Reply in JSON" gave **0/20** usable results, even though the JSON itself looked fine
- What a retry, a regex hack and structured outputs each cost, and what each one actually guarantees
- Why **schema-valid is not the same as correct**, and how to check the values

## Quickstart
Needs an Anthropic API key. A full run costs **a few cents** on Claude Haiku 4.5.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/01-genai-llm-foundations/04-structured-outputs
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
cp .env.example .env        # then paste your key
jupyter notebook notebook.ipynb
```

## Results from a real run (Claude Haiku 4.5, 20 tickets)

| Approach | Usable (schema-valid) | API calls | Median time | Avg output tokens | Cost |
|---|---|---|---|---|---|
| "Reply in JSON" | **0/20** | 20 | 0.89 s | 73 | $0.0086 |
| + strip fences / grab `{...}` | **0/20** | same | | | |
| Schema in prompt, first try | **0/20** | 20 | | | |
| Schema in prompt + 1 retry | **10/20** | 40 | 1.53 s | 125 | $0.0267 |
| Schema in prompt + strip fences | **20/20** | 20 | 0.81 s | 68 | $0.0128 |
| **Structured outputs** | **20/20** | 20 | 0.94 s | **47** | $0.0157 |

- **Why the failures happened:** every non-structured response (20/20) came wrapped in ```` ```json ```` fences, even when told "no code fences". "Reply in JSON" also invented its own values (`"Billing"`, `"High"`, `"$49.99"` as a string).
- **Valid ≠ correct:** structured outputs got all **60/60** objective fields right (order id, refund amount, email), but agreed with the hand labels on **18/20** for priority and **14/20** for sentiment.
- **Retries vary:** the retry results change from run to run, because the fences appear unpredictably.

## Files
- `notebook.ipynb`: the walkthrough, committed with its outputs
- `data/tickets.json`: the 20 tickets and their hand-written labels
- `findings.json`: the numbers above, written by the last cell
- `.env.example`: copy to `.env` and add your key (`.env` is git-ignored)
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups

**Builds on:** [03 · Your first LLM API call](../03-first-llm-api-call/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. Next: [05 · Context windows and cost](../05-context-windows-and-cost/).
