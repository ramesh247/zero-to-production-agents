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

## 05 · Context windows, tokens and what your prompt really costs ([full pack](05-context-windows-and-cost/INTERVIEW.md))

| Level | Question |
|---|---|
| Junior | Same data, same model. Why did one prompt cost 2.4× more than another? |
| Junior | YAML is more compact than JSON, right? |
| Mid ⭐ | Your chatbot's 10th message sends 80× the input tokens of its 1st. Why? |
| Mid | Which costs more: the prompt you send or the answer you get? |
| Mid | How do you know what a request will cost before you send it? |
| Senior | The model has a 200K-token context window. Can you just paste in all your tickets? |
| Senior | Two chat answers came back exactly 400 tokens long. Coincidence? |
| Senior | A sliding window saved 61% of input tokens. What did it cost you? |

## 06 · Prompt caching ([full pack](06-prompt-caching/INTERVIEW.md))

| Level | Question |
|---|---|
| Junior | You added `cache_control` and nothing changed. Why? |
| Junior | Is the first cached request cheaper? |
| Mid ⭐ | You put the current time at the top of your system prompt. What does that do to caching? |
| Mid | How much did caching save on 10 questions? |
| Mid | Does prompt caching make responses faster? |
| Senior | What exactly gets cached, and where do you put the breakpoint? |
| Senior | Your app sends the same prompt once every 10 minutes. Should you cache it? |
| Senior | Why does the notebook put a random run id at the start of the system prompt? |

## 07 · Images and PDFs as LLM input ([full pack](07-multimodal-inputs/INTERVIEW.md))

| Level | Question |
|---|---|
| Junior | How many tokens does an image cost? |
| Junior ⭐ | Should you send images at full resolution so the model can read them? |
| Mid | The image was too small to read. What did the model do? |
| Mid | You extract a PDF's text with a library and send that. What do you lose? |
| Mid | What changes when you send the PDF itself instead? |
| Senior | Your pipeline processes 100,000 invoices a month. Where does the money go? |
| Senior | Why does the notebook turn thinking off? |
| Senior | A user uploads a photo of a receipt taken at an angle in bad light. What breaks first? |
