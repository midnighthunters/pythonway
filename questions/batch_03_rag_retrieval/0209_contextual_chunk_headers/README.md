# Q0209 · Contextual chunk headers

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Chunking | Medium |

## Question

Implement "contextual" chunk text for embedding: prepend the document title, section path and effective date to each chunk before embedding, while keeping the raw text for display and citation.

## Answer

```python
def contextualize(chunk: dict, doc: dict) -> dict:
    header = f"Document: {doc['title']}\nSection: {chunk['headings']}\nEffective: {doc['effective']}"
    return {**chunk, "embed_text": f"{header}\n\n{chunk['text']}", "display_text": chunk["text"]}


doc = {"title": "UK Travel & Expenses Policy", "effective": "2026-04-01"}
c = contextualize({"headings": "Hotels > London", "text": "Cap is 180 GBP per night."}, doc)
assert c["embed_text"].startswith("Document: UK Travel & Expenses Policy\nSection: Hotels > London")
assert c["display_text"] == "Cap is 180 GBP per night."
```

Why it helps: chunks often lack context ("the cap", "this policy"). Adding the title and section makes the embedding and BM25 match queries like "UK hotel limit London". A more expensive variant is to have an LLM write a one-sentence "situating context" for each chunk given the whole document (contextual retrieval), which improves recall further at a one-off ingestion cost.

Keep the header short, or it dominates the embedding of small chunks.

## Likely follow-ups

- How would you measure whether contextual headers improved retrieval?

---

[← Q0208](../../batch_03_rag_retrieval/0208_sentence_window_retrieval/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0210 →](../../batch_03_rag_retrieval/0210_document_parsing_challenges/README.md)
