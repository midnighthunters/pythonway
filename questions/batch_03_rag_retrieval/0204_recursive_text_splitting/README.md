# Q0204 · Recursive text splitting

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Chunking | Medium |

## Question

Implement a recursive splitter: try to split on paragraphs, then lines, then sentences, then spaces, packing pieces up to `max_len` characters, and only hard-cut as a last resort.

## Answer

```python
def recursive_split(text: str, max_len: int, seps: tuple[str, ...] = ("\n\n", "\n", ". ", " ")) -> list[str]:
    if len(text) <= max_len:
        return [text] if text.strip() else []
    for i, sep in enumerate(seps):
        if sep not in text:
            continue
        chunks, cur = [], ""
        for part in text.split(sep):
            candidate = part if not cur else cur + sep + part
            if len(candidate) <= max_len:
                cur = candidate
                continue
            if cur:
                chunks.append(cur)
            if len(part) > max_len:
                chunks.extend(recursive_split(part, max_len, seps[i + 1:]))
                cur = ""
            else:
                cur = part
        if cur:
            chunks.append(cur)
        return [c for c in chunks if c.strip()]
    return [text[j:j + max_len] for j in range(0, len(text), max_len)]


doc = ("Travel policy.\n\nFlights over six hours may be booked in business class. Approval is needed. "
       "Hotels are capped per city.\n\nExpenses must be filed within 30 days.")
chunks = recursive_split(doc, 60)
assert all(len(c) <= 60 for c in chunks)
assert chunks[0] == "Travel policy."
assert chunks[-1] == "Expenses must be filed within 30 days."
assert recursive_split("x" * 25, 10) == ["x" * 10, "x" * 10, "x" * 5]
```

This is the idea behind LangChain's `RecursiveCharacterTextSplitter`: keep natural units together whenever they fit. Measure chunk sizes in tokens in production.

## Likely follow-ups

- Why is splitting on ". " imperfect (abbreviations, decimals)?

---

[← Q0203](../../batch_03_rag_retrieval/0203_fixed_size_chunking_with_overlap/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0205 →](../../batch_03_rag_retrieval/0205_structure_aware_chunking_of_markdown/README.md)
