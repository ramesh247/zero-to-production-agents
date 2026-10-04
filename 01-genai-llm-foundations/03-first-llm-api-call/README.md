# 03 · Your first LLM API call, done properly

The 3-line LLM call from every tutorial works in a demo. This notebook makes it production-ready, measuring each step against the real Claude API: reading `stop_reason` and usage, streaming, which errors to retry, how many retries, and timeouts.

**What you'll learn**
- Why a **200 OK can still be a broken answer**, and the one field that tells you
- Why streaming doesn't make the model faster but **does survive a 2-second timeout** that kills the blocking call
- Which errors to retry, how many times, and what each retry costs in time

## Quickstart
Needs an Anthropic API key. The whole notebook costs **a few cents** on Claude Haiku 4.5, and errors aren't billed.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/01-genai-llm-foundations/03-first-llm-api-call
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
cp .env.example .env        # then paste your key
jupyter notebook notebook.ipynb
```

## Results from a real run (Claude Haiku 4.5, `anthropic` SDK 1.11)

| Experiment | Result |
|---|---|
| Streaming vs not (median of 5, ~258 tokens) | First text **0.60 s vs 3.03 s**; total **3.05 s vs 3.03 s** |
| `max_tokens=25` | **HTTP 200**, `stop_reason: max_tokens`, no exception, cut mid-sentence |
| 404 / 400 / 401 | 1 attempt each: the SDK doesn't retry them |
| Unreachable server | 3 attempts (default `max_retries=2`) |
| 2 s timeout, ~600-word answer | Non-streaming: **`APITimeoutError` at 2.04 s**. Streaming: **ok, 1,055 tokens in 12.2 s** |

**Retries** (40 requests; 17 hit an **injected** 429/529, retried by the SDK itself):

| `max_retries` | Succeeded | Time |
|---|---|---|
| 0 | 23/40 | 13.7 s |
| 2 | 38/40 | 31.1 s |
| 4 | 40/40 | 41.6 s |

## Files
- `notebook.ipynb`: the walkthrough, committed with its outputs
- `findings.json`: the numbers above, written by the last cell
- `.env.example`: copy to `.env` and add your key (`.env` is git-ignored)
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups

**Builds on:** [01 · Tokens](../01-tokens-and-embeddings/) (what you pay for) and [02 · Sampling](../02-sampling-parameters/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. Next: [04 · Getting reliable JSON out of an LLM](../README.md).
