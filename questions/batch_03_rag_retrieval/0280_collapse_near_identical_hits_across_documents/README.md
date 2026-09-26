# Q0280 · Collapse near-identical hits across documents

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Context assembly | Medium |

## Question

The same paragraph appears in several documents (a policy copied into team pages). Collapse near-identical retrieved chunks into one, keeping the highest-scoring copy and recording where else it appears.

## Answer

```python
from difflib import SequenceMatcher


def collapse_duplicates(hits: list[dict], threshold: float = 0.9) -> list[dict]:
    kept: list[dict] = []
    for h in sorted(hits, key=lambda h: -h["score"]):
        for k in kept:
            if SequenceMatcher(None, h["text"].lower(), k["text"].lower()).ratio() >= threshold:
                k["also_in"].append(h["doc_id"])
                break
        else:
            kept.append({**h, "also_in": []})
    return kept


hits = [{"doc_id": "wiki-3", "score": 0.80, "text": "Hotels in London are capped at 180 GBP per night."},
        {"doc_id": "pol-7", "score": 0.85, "text": "Hotels in London are capped at 180 GBP per night"},
        {"doc_id": "faq-1", "score": 0.60, "text": "Claims must be filed within 30 days."}]
out = collapse_duplicates(hits)
assert [(h["doc_id"], h["also_in"]) for h in out] == [("pol-7", ["wiki-3"]), ("faq-1", [])]
```

Keeping the authoritative copy (combine this with source priors) and noting the duplicates frees context budget for diverse evidence. Pairwise comparison is O(k²), which is fine for top-k lists. Use MinHash at ingestion for corpus-wide deduplication.

## Likely follow-ups

- Which copy should win when the scores are equal but the sources differ in authority?

---

[← Q0279](../../batch_03_rag_retrieval/0279_calibrate_a_retrieval_score_threshold/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0281 →](../../batch_03_rag_retrieval/0281_document_versioning_in_the_index/README.md)
