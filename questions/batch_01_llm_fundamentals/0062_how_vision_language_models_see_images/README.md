# Q0062 · How vision-language models see images

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Multimodal | Medium |

## Question

How does a multimodal LLM process an image, and what are the practical implications for a document-heavy enterprise?

## Answer

- A vision encoder (often a ViT) splits the image into patches and produces patch embeddings. A projector maps them into the LLM's token-embedding space, so the image becomes a sequence of "visual tokens" interleaved with text.
- High-resolution handling usually tiles the image into crops plus a low-resolution overview, so the token count grows with resolution.

Implications:
- Cost and latency scale with image size and detail setting, and a scanned 50-page PDF can be very expensive.
- For text-heavy documents, dedicated OCR or layout extraction plus text RAG is usually cheaper and more accurate. Use vision models for charts, forms, handwriting, screenshots and layout questions.
- Small text, tables and numbers are error-prone, so validate extracted figures, especially financial ones.
- Security: images can carry injected instructions (text in the image), which is a multimodal prompt-injection vector.

## Likely follow-ups

- How would you extract tables from scanned bank statements reliably?

---

[← Q0061](../../batch_01_llm_fundamentals/0061_choosing_an_embedding_model/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0063 →](../../batch_01_llm_fundamentals/0063_estimate_image_token_cost/README.md)
