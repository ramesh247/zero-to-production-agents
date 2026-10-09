# Interview pack: images and PDFs as LLM input

Every answer is backed by a number from [notebook.ipynb](notebook.ipynb), run on **Claude Haiku 5.5** with thinking
turned off ($0.10 / $0.50 per million input / output tokens for prompts up to 100K tokens). The test inputs are a
synthetic 20-line invoice image (62 values to read) and a 3-page PDF report whose chart and table are embedded as images.
Each image size and each PDF mode ran 3 times.

---

### 1. How many tokens does an image cost? · Junior
- **Trap:** "A fixed amount per image, like a short message."
- **Answer:** It scales with the pixels. The same invoice cost **5,337 input tokens at 2400×3000** and **833 at 400×500** (both counts include the short text prompt). That's 84% fewer tokens for the same document.
- **Follow-up:** How do you find out for your own images?
- **Follow-up answer:** `messages.count_tokens` with the image in the message. It doesn't charge per call, so measure a few sizes before you pick one.
- Notebook: [§1](notebook.ipynb#1-an-invoice-five-image-sizes)

### ⭐ 2. Should you send images at full resolution so the model can read them? · Junior
- **Trap:** "Yes. More pixels, better accuracy."
- **Answer:** Not past the point it can read them. The invoice came back **62/62 correct at every size from 2400×3000 down to 400×500**, and 400×500 used 84% fewer tokens. Accuracy only fell below that: **56-57/62 at 300×375**, **21-22 at 240×300**, **2-5 at 200×250**.
- **Follow-up:** How would you choose the size in production?
- **Follow-up answer:** Run your real documents at a few sizes against known values, find where accuracy starts to drop, and ship a step above it for margin. The cut-off depends on the smallest text in your documents, not on the image as a whole.
- Notebook: [§1](notebook.ipynb#1-an-invoice-five-image-sizes)

### 3. The image was too small to read. What did the model do? · Mid
- **Trap:** "It says it can't read it."
- **Answer:** It guessed, quietly. At 300×375 it returned all 20 lines in valid JSON with `stop_reason: end_turn` and no warning, but some numbers were wrong: **90.15 came back as 90.10, 62.54 as 62.64**. The total was still right, so a spot-check on the total would have passed.
- **Follow-up:** How do you catch that?
- **Follow-up answer:** Cross-check the numbers against each other: qty × unit price should equal the amount, and the amounts should sum to the total. Business-rule checks catch misreads that the schema can't (build #004: valid is not correct).
- Notebook: [§1](notebook.ipynb#1-an-invoice-five-image-sizes)

### 4. You extract a PDF's text with a library and send that. What do you lose? · Mid
- **Trap:** "Nothing. The text is the content."
- **Answer:** Everything that's a picture. `pypdf` extracted the text page perfectly, so the 4 text questions were **12/12 correct**. But the chart and the scanned table are images, so the 4 questions about them got **0/12**: the model answered null every time.
- **Follow-up:** Why null and not a guess?
- **Follow-up answer:** The prompt allowed null for "not in the document", and the extracted text clearly had nothing for those questions. Give the model an explicit way to say "not found", or it's more likely to invent something.
- Notebook: [§2](notebook.ipynb#2-a-pdf-whose-numbers-live-in-pictures)

### 5. What changes when you send the PDF itself instead? · Mid
- **Trap:** "The API just extracts the text for you."
- **Answer:** The model gets each page as text **and** as an image. Sending the PDF as a `document` block got **24/24** answers right, including all 12 from the chart and the scan. It cost **5,413 input tokens vs 678** for the extracted text, about **$0.0006 vs $0.0001** per question set.
- **Follow-up:** So always send the PDF?
- **Follow-up answer:** Not for text-only documents, where extraction gave the same 12/12 for an eighth of the tokens. Send the PDF when it has charts, scans or layout that carry meaning, or route by checking whether pages contain images.
- Notebook: [§2](notebook.ipynb#2-a-pdf-whose-numbers-live-in-pictures)

### 6. Your pipeline processes 100,000 invoices a month. Where does the money go? · Senior
- **Trap:** "Output tokens. They're 5× the price."
- **Answer:** Check the size first. Per call, input cost was **$0.000534 at 2400×3000** (5,337 tokens × $0.10/M) and **$0.000083 at 400×500**. The structured output was about 765 tokens of JSON at every readable size, $0.00038 per call, so it went from about 40% of the cost at full size to over 80% at 400×500. At this volume, both are worth measuring.
- **Follow-up:** What else would you change at that volume?
- **Follow-up answer:** The Batch API for invoices that don't need an instant answer (half price), and only the fields you actually use in the schema: fewer output tokens per invoice.
- Notebook: [§1](notebook.ipynb#1-an-invoice-five-image-sizes)

### 7. Why does the notebook turn thinking off? · Senior
- **Trap:** "Thinking always makes answers better, so leave it on."
- **Answer:** Claude Haiku 5.5 thinks by default, and thinking tokens are billed as output. Reading values off an invoice is transcription, not reasoning, and with thinking off it already got 62/62 down to 400×500, so there was nothing left for thinking to fix. I didn't run it with thinking on, so I can't say what it would have cost here.
- **Follow-up:** When would you turn it back on?
- **Follow-up answer:** When the task needs reasoning over what was read: reconciling two documents, spotting inconsistencies, answering questions that combine several values. Measure it per task (build #008 compares models and settings).
- Notebook: [setup](notebook.ipynb#beyond-text-images-and-pdfs-as-llm-input)

### 8. A user uploads a photo of a receipt taken at an angle in bad light. What breaks first? · Senior
- **Trap:** "The model handles photos fine, it's multimodal."
- **Answer:** This notebook can't tell you: it tested clean, synthetic images, plus one scan rotated by 1.2° (which read correctly). What it does show is how the model fails when it can't read well: **plausible wrong numbers, no error**. Expect the same with blur and glare.
- **Follow-up:** How would you test it properly?
- **Follow-up answer:** Build a small labelled set of real photos (angles, lighting, crumpled paper), measure field accuracy as in §1, and add the arithmetic checks from question 3 before trusting any extracted total.
- Notebook: [§1](notebook.ipynb#1-an-invoice-five-image-sizes), [§2](notebook.ipynb#2-a-pdf-whose-numbers-live-in-pictures)
