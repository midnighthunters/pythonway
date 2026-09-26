# Q0210 · Document parsing challenges

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Ingestion | Medium |

## Question

What goes wrong when parsing enterprise PDFs, slide decks and scanned documents for RAG, and how do you handle it?

## Answer

Problems:
- Reading order: multi-column layouts, sidebars and footnotes get interleaved.
- Tables flatten into word soup, losing the row and column relationships.
- Headers, footers and page numbers repeat on every page (noise that matches many queries).
- Scans and images need OCR, with errors in numbers.
- Hyphenation and line-break artefacts, and ligatures.
- Slide decks: fragmented bullets and important content in diagrams.
- Embedded or attached files, and password-protected documents.

Handling:
- Use layout-aware parsers (or document-intelligence services such as Azure AI Document Intelligence or Amazon Textract) that output structure: headings, paragraphs, tables and reading order.
- Convert tables to structured text (row-wise "column: value" lines) or keep them as markdown, and store them separately if large.
- Strip repeated boilerplate, and normalise hyphenation and Unicode.
- Keep page numbers as metadata for citations.
- Measure parsing quality on a sample (spot checks and retrieval evaluations), and route failures to a quarantine for review.

## Likely follow-ups

- How would you detect that a document parsed badly without reading it?

---

[← Q0209](../../batch_03_rag_retrieval/0209_contextual_chunk_headers/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0211 →](../../batch_03_rag_retrieval/0211_remove_repeated_headers_and_footers/README.md)
