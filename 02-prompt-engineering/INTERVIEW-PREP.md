# Interview prep: Prompt Engineering

Every question comes with a trap answer, a real answer backed by a notebook run, and a follow-up.

## 01 · Anatomy of a production prompt ([full pack](01-anatomy-of-a-prompt/INTERVIEW.md))

| Level | Question |
|---|---|
| Junior | Which part of a prompt matters most: role, context, task or format? |
| Junior | With only the task in the prompt, the model scored 13%. Was it bad at triage? |
| Mid ⭐ | The model's answer was right, but your pipeline rejected it. How? |
| Mid | You wrote the rubric by looking at the dev tickets. Isn't +30 points just overfitting? |
| Mid | The rubric made the prompt 3× longer. Did it make it 3× more expensive? |
| Senior | The full prompt still misses on 25% of test runs. Where? |
| Senior | Your PM wants to add "You are a world-class support expert. Be accurate." Will it help? |
| Senior | Is a 2-point gain real or noise? |

## 02 · Zero-shot vs few-shot ([full pack](02-zero-vs-few-shot/INTERVIEW.md))

| Level | Question |
|---|---|
| Junior | More examples, better results? |
| Mid ⭐ | Your prompt misses edge cases. Add examples or fix the rules? |
| Mid | Can you skip writing the rules and just show examples? |
| Mid | All 4 of your examples are labelled "high". Does the model start saying "high" for everything? |
| Senior | A rule fix made a ticket that used to pass fail. How? |
| Senior | One ticket was wrong in every single prompt. Whose fault? |
| Senior | 85% vs 78%. Is the improvement real? |
| Senior | Rubric v2 scored 100% on build #009's test set. Why isn't that the headline? |

## 03 · Chain-of-thought and extended thinking ([full pack](03-chain-of-thought/INTERVIEW.md))

| Level | Question |
|---|---|
| Junior | Does "think step by step" make the model more accurate? |
| Junior | Does thinking slow down easy questions too? |
| Mid ⭐ | You told the model "reply with only the answer". Why did it write 3,251 tokens? |
| Mid | Extended thinking must be much more expensive, right? |
| Mid | Which effort level would you ship? |
| Senior | Should you turn on thinking for ticket triage? |
| Senior | Visible reasoning and built-in thinking used about the same tokens. Why such different accuracy? |
| Senior | Product wants these catalog answers in under 1 second. What do you say? |
