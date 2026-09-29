# 01 · What an LLM actually sees: tokens and embeddings

An LLM never reads your words. It reads token IDs and turns them into vectors. This notebook measures both steps, using 4 real tokenizers and a multilingual embedding model.

**What you'll learn**
- Why `"Hello"` and `" Hello"` are different inputs, and why `2026` is two tokens
- Why the same meaning costs **64% more tokens in Spanish** on GPT-4's tokenizer, and how a bigger vocabulary changes that
- What embeddings get right (cross-language meaning) and where they still get fooled by shared words

## Quickstart
No API key is needed, and the notebook costs $0 to run. The first run downloads about 0.5 GB of model files.
```sh
git clone https://github.com/ramesh247/zero-to-production-agents.git
cd zero-to-production-agents/01-genai-llm-foundations/01-tokens-and-embeddings
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
jupyter notebook notebook.ipynb
```

## Results from a real run

**Same 8 sentences, English vs Spanish** (Spanish is 15% longer in characters):

| Tokenizer | EN tokens | ES tokens | ES / EN |
|---|---|---|---|
| GPT-4 (`cl100k_base`) | 92 | 151 | 1.64 |
| GPT-4o (`o200k_base`) | 92 | 128 | 1.39 |
| Qwen2.5 | 92 | 151 | 1.64 |
| XLM-R (multilingual) | 111 | 138 | 1.24 |

**Embedding similarity to an anchor sentence** (mean of 3 sets, `paraphrase-multilingual-MiniLM-L12-v2`):

| Candidate | Cosine | Word overlap |
|---|---|---|
| Spanish translation | 0.87 | 0.00 |
| Same words, different meaning | 0.67 | 0.66 |
| Paraphrase, no shared words | 0.66 | 0.11 |
| Unrelated | 0.04 | 0.00 |

The surprise: in one set, "The deployment **of troops** failed because of a timeout in talks" scored **0.90**, higher than a real paraphrase (0.51).

## Files
- `notebook.ipynb`: the walkthrough, committed with its outputs
- `data/sentences.json`: every sentence used (a few KB)
- `findings.json`: the numbers above, written by the last cell
- [`INTERVIEW.md`](INTERVIEW.md): 8 interview questions, each with a trap answer, a real answer and a follow-up, backed by this run

---
Part of [The Agent Build Log](../../README.md): follow the series on LinkedIn. Next: [02 · Temperature, top-p, top-k](../README.md).
