# Q0294 · RAG over scanned and image-heavy documents

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Multimodal RAG | Medium |

## Question

Much of the corpus is scanned PDFs, charts and slides. What are your options for making it retrievable and answerable?

## Answer

1. OCR plus layout extraction (for example Azure AI Document Intelligence or Amazon Textract), then text RAG. It is cheap at query time and searchable, but loses chart meaning. Check OCR quality (confidence scores) and route low-confidence pages to review.
2. Vision-LLM captioning at ingestion: generate text descriptions of charts, diagrams and slides and index them, with links to the page image. Good recall for visual content, at a one-off ingestion cost.
3. Multimodal embeddings (image and text in one space), or page-image retrieval with late-interaction vision models (the ColPali style), which retrieve page images directly.
4. At answer time, send the retrieved page images to a vision-capable model for questions about charts or tables.

Controls: keep page numbers and images for citations, verify extracted numbers, and watch cost (image tokens). Hidden text in images is an injection vector.

## Likely follow-ups

- When would you pay for page-image retrieval instead of OCR text?

---

[← Q0293](../../batch_03_rag_retrieval/0293_interleaving_tests_for_retrievers/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0295 →](../../batch_03_rag_retrieval/0295_invalidate_cached_answers_on_document_change/README.md)
