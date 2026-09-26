# Q0212 · Tables in RAG

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Ingestion | Medium |

## Question

How should tables be represented for retrieval and generation? Implement a row-to-text linearisation that keeps headers with every value.

## Answer

```python
def linearize_table(caption: str, header: list[str], rows: list[list[str]]) -> list[str]:
    out = []
    for row in rows:
        if len(row) != len(header):
            raise ValueError(f"row has {len(row)} cells, header has {len(header)}")
        cells = "; ".join(f"{h}: {v}" for h, v in zip(header, row))
        out.append(f"{caption} | {cells}")
    return out


lines = linearize_table("Hotel caps by city (2026)", ["City", "Cap", "Currency"],
                        [["London", "180", "GBP"], ["New York", "300", "USD"]])
assert lines[1] == "Hotel caps by city (2026) | City: New York; Cap: 300; Currency: USD"
```

Options:
- Row-wise linearisation (as above): each row becomes a retrievable unit that is self-describing. Good for lookup questions.
- Whole table as markdown in one chunk: good for comparison questions when the table is small.
- Tables into a SQL store with text-to-SQL: best for aggregations ("average cap across EMEA").
- Summaries of large tables for retrieval, pointing to the full table.

Keep numbers exact, and include units and currency in the header, because models and embeddings lose them easily.

## Likely follow-ups

- A question asks for "the highest cap in Europe". Which representation answers it best?

---

[← Q0211](../../batch_03_rag_retrieval/0211_remove_repeated_headers_and_footers/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0213 →](../../batch_03_rag_retrieval/0213_deduplicate_near_duplicate_chunks_with_minhash/README.md)
