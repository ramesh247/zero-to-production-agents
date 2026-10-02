# 02 · Temperature, top-p, top-k: a visual guide to sampling

At every step an LLM scores all 151,665 tokens in its vocabulary, and a sampling strategy picks one. This notebook measures what temperature, top-k and top-p actually do to that choice, using a small open model.

**What you'll learn**
- Why temperature 0 loops, and why a "low" temperature still isn't deterministic
- How top-p adapts to the model's confidence while top-k doesn't, and why top-p **doesn't** rescue a high temperature
- How to choose sampling settings with numbers (variety vs readability) instead of copying 0.7

## Quickstart
No API key is needed, and the notebook costs $0 to run on a laptop CPU. The first run downloads Qwen2.5-0.5B, about 1 GB.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/01-genai-llm-foundations/02-sampling-parameters
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
jupyter notebook notebook.ipynb
```

## Results from a real run (Qwen2.5-0.5B)

**How many tokens it takes to cover 90% of the probability** (prompt: "The best programming language for beginners is"):

| Temperature | Top token | Tokens for 90% |
|---|---|---|
| 0.2 | 86.5% | 2 |
| 0.7 | 32.9% | 12 |
| 1.0 | 18.1% | 77 |
| 1.5 | 5.3% | 5,951 |
| 2.0 | 1.4% | 35,971 |

**Same prompt, 10 samples per setting** ("Three tips for writing clean code"):

| Setting | Distinct (of 10) | Distinct-2 | Repeat-4 | Avg logprob |
|---|---|---|---|---|
| greedy (T=0) | 1 | 0.06 | 0.22 | −0.66 |
| T=0.7 | 10 | 0.81 | 0.01 | −2.23 |
| T=1.0, top-p=0.9 | 10 | 0.94 | 0.01 | −2.53 |
| T=1.5 | 10 | 1.00 | 0.00 | −9.83 |
| T=1.5, top-p=0.9 | 10 | 1.00 | 0.00 | −8.52 |

The surprise: **top-p=0.9 at T=1.5 still allowed 10,995 candidate tokens** on an open-ended prompt, and the output was gibberish either way.

## Files
- `notebook.ipynb`: the walkthrough, committed with its outputs
- `data/prompts.json`: the prompts and the 8 settings
- `findings.json`: the numbers above, written by the last cell
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups

**Builds on:** [01 · Tokens and embeddings](../01-tokens-and-embeddings/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. Next: [03 · Your first LLM API call](../README.md).
