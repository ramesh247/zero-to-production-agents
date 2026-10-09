# 05 · Context windows, tokens and what your prompt really costs

Where do the tokens in a real LLM bill come from? This notebook measures the four biggest drivers on Claude Haiku 4.5: how you format data, how chat history grows, how long answers are, and what actually fits in the context window.

**What you'll learn**
- Why the same data can cost **2.4× more** depending on format, and why YAML isn't the compact option it looks like
- Why a chatbot's 10th turn sends 80× the input tokens of its 1st, and what a sliding window saves
- Why **output length**, not your prompt, is usually most of the bill

## Quickstart
Needs an Anthropic API key. A full run costs **a few cents**; most measurements use `count_tokens`, which doesn't charge per call.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/01-genai-llm-foundations/05-context-windows-and-cost
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
cp .env.example .env        # then paste your key
jupyter notebook notebook.ipynb
```

## Results from a real run (Claude Haiku 4.5)

**Same 20 support tickets (from build #004), five formats:**

| Format | Tokens | vs CSV | Tickets per 200K window |
|---|---|---|---|
| CSV | 863 | 1.00× | 4,629 |
| Markdown table | 1,046 | 1.21× | 3,824 |
| JSON, minified | 1,393 | 1.61× | 2,873 |
| YAML | 1,584 | 1.84× | 2,525 |
| JSON, pretty (indent=2) | 2,091 | 2.42× | 1,912 |

**A real 10-turn chat:** billed input went from **46 tokens (turn 1) to 3,660 (turn 10)**, **18,441** in total. Keeping only the last 2 exchanges would send **7,261 (−61%)**. That's a token count; answer quality with trimmed history wasn't tested. `count_tokens` matched the billed input on every turn.

**Output length:** with no instruction, output was **99.2%** of the cost. "Answer in at most two sentences" cut output from **368.8 to 74.2 tokens**, cost per answer from **$0.001859 to $0.000393**, and time from **4.20 s to 1.22 s**.

## Files
- `notebook.ipynb`: the walkthrough, committed with its outputs
- `data/tickets.json`: the 20 tickets from build #004
- `findings.json`: the numbers above, written by the last cell
- `.env.example`: copy to `.env` and add your key (`.env` is git-ignored)
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups

**Builds on:** [01 · Tokens](../01-tokens-and-embeddings/) and [04 · Reliable JSON](../04-structured-outputs/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. Next: [06 · Prompt caching](../06-prompt-caching/).
