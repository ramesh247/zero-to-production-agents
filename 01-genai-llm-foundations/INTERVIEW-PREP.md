# Interview prep: GenAI & LLM Foundations

Every question comes with a trap answer, a real answer backed by a notebook run, and a follow-up.
⭐ marks the trickiest question in each project.

## 01 · Tokens and embeddings ([full pack](01-tokens-and-embeddings/INTERVIEW.md))

| Level | Question |
|---|---|
| Junior | `"Hello"` vs `" Hello"`: are they the same token? |
| Junior | How many tokens is `2026`? |
| Mid | Why is 🔥🚀 3 tokens and 👨‍👩‍👧 8 tokens? |
| Mid | Can you estimate one model's token count with another model's tokenizer? |
| Mid ⭐ | You launch your English app in Spanish with the same prompts. What happens to token cost? |
| Senior | Your semantic search matched a sentence about troops to a question about a failed software deployment. What went wrong? |
| Senior | A user asks in Spanish; your documents are in English. Do you have to translate before retrieving? |
| Senior | Does the word "bank" have one embedding? |

## 02 · Temperature, top-p, top-k ([full pack](02-sampling-parameters/INTERVIEW.md))

| Level | Question |
|---|---|
| Junior | What does temperature = 0 actually do? |
| Junior | Does a higher temperature let the model use new words? |
| Mid | top-k vs top-p: what's the difference? |
| Mid ⭐ | You set top-p = 0.9 as a safety net, so T = 1.5 is safe, right? |
| Mid | The model says the best language for beginners is C. Is that its opinion? |
| Senior | Your agent repeats the same step over and over at temperature 0. Why? |
| Senior | How do you choose a temperature with data instead of gut feel? |
| Senior | Your code sets temperature=0, and the new model's API rejects it. What now? |

## 03 · Your first LLM API call, done properly ([full pack](03-first-llm-api-call/INTERVIEW.md))

| Level | Question |
|---|---|
| Junior | Your call returned 200 OK, but the answer stops mid-sentence. What happened? |
| Junior | Does streaming make the model faster? |
| Junior | How do you know what one call cost? |
| Mid | Which errors should you retry? |
| Mid ⭐ | How many retries should you configure? |
| Mid | You set a 2-second timeout to keep the app snappy. What breaks? |
| Senior | Your bug report says "the LLM call failed". What do you need to debug it? |
| Senior | After upgrading the SDK, a call with `temperature` fails before reaching the API. Why? |

## 04 · Getting reliable JSON out of an LLM ([full pack](04-structured-outputs/INTERVIEW.md))

| Level | Question |
|---|---|
| Junior | You asked for JSON and got JSON. Why did `json.loads` fail on every response? |
| Junior | After stripping the fences, the JSON still failed validation. Why? |
| Mid | Does retrying with the error message fix bad JSON? |
| Mid ⭐ | Structured outputs gave you 20/20 valid JSON. Is the data correct? |
| Mid | Is structured outputs the cheapest option? |
| Senior | The first structured-output call was twice as slow as the rest. Why? |
| Senior | Your schema says `refund_amount` must be ≥ 0. Will the API enforce it? |
| Senior | One ticket is in Spanish. Do you need a separate pipeline? |
