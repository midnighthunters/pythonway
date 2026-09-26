# Q0202 · When not to use RAG

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | RAG architecture | Medium |

## Question

When is RAG the wrong tool, and what would you use instead?

## Answer

- Structured, numeric questions ("total spend by cost centre last quarter"): use text-to-SQL or an API tool against the system of record, not chunks of reports.
- Tasks on one known document ("summarise this contract"): pass the whole document to a long-context model, or use map-reduce. No retrieval is needed.
- Behaviour and format gaps (house style, classification labels): prompting or fine-tuning.
- Real-time data (balances, prices, statuses): call live tools. Indexed copies go stale.
- Tiny, stable knowledge (ten FAQs): put it in the prompt (and cache it).
- Actions (book, submit, approve): tools with authorisation, not retrieval.

Many assistants need a router that picks between RAG, SQL, tools and direct answers per request.

## Likely follow-ups

- How would you route between RAG and text-to-SQL automatically?

---

[← Q0201](../../batch_03_rag_retrieval/0201_rag_end_to_end/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0203 →](../../batch_03_rag_retrieval/0203_fixed_size_chunking_with_overlap/README.md)
