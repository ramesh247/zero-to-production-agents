# 08 · 7 prompt anti-patterns and how to fix them

Seven habits from real prompts, each measured against its fix on 20 labelled support tickets: a vague task, conflicting instructions, SHOUTING, only saying what not to do, a broken format example, padding with unrelated context, and trusting the model's confidence score. Some hurt a lot. Some barely mattered.

**What you'll learn**
- Why a broken example (single quotes, trailing comma) made **75%** of replies invalid JSON
- Why IMPORTANT!!! in capitals changed nothing measurable
- What 10K tokens of "context, just in case" did to accuracy (nothing) and cost (**13×**)

## Quickstart
Needs an Anthropic API key. A full run (720 calls) costs about **13 cents** on Claude Haiku 5.5.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/02-prompt-engineering/08-prompt-anti-patterns
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
cp .env.example .env        # then paste your key
jupyter notebook notebook.ipynb
```

## Results from a real run (Claude Haiku 5.5, thinking off, 20 tickets × 3 runs)

| Anti-pattern | With it | With the fix |
|---|---|---|
| 1. Vague task ("What do you think?") | 2% usable, 0% right | 100% usable, **90%** right |
| 2. Conflicting instructions | 67% of replies under 50 words | 82% |
| 3. SHOUTING | 100% usable, 85% right | 100% usable, 90% right |
| 4. Only "Don't use markdown" | 5% with markdown (20% with no instruction) | 0% |
| 5. Broken format example | **25%** valid JSON | 100% |
| 6. 10K tokens of unrelated context | 90% right, **$1.113** per 1,000 tickets | 90% right, $0.085 |
| 7. Trusting a confidence score | right answers averaged 88.5, wrong 82.5 | none of the 6 wrong answers scored ≥ 90, but only 18 of 50 right ones did |

## Files
- `notebook.ipynb`: the walkthrough, committed with its outputs
- `data/tickets.json`, `data/rubric_v3.md`: build #014's test tickets and best prompt
- `findings.json`: the numbers above, written by the last cell
- `.env.example`: copy to `.env` and add your key (`.env` is git-ignored)
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions with trap answers, real answers and follow-ups

**Builds on:** everything in this subject, especially [01](../01-anatomy-of-a-prompt/), [06](../06-eval-driven-prompting/) and [07](../07-prompt-versioning/)

---
Part of [Zero to Production Agents](../../README.md), the code behind The Agent Build Log on LinkedIn. This closes subject 02. Next: [03 · RAG systems](../../03-rag-systems/).
