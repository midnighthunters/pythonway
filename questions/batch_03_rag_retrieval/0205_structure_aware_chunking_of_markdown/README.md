# Q0205 · Structure-aware chunking of markdown

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Chunking | Medium |

## Question

Chunk a markdown or HTML-derived document by headings, so each chunk carries its heading path (for example "Travel > Hotels > London"). Why does this improve retrieval?

## Answer

```python
import re


def chunk_markdown(md: str) -> list[dict]:
    path: list[tuple[int, str]] = []
    chunks: list[dict] = []
    buf: list[str] = []

    def flush() -> None:
        body = "\n".join(buf).strip()
        if body:
            chunks.append({"headings": " > ".join(h for _, h in path), "text": body})
        buf.clear()

    for line in md.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush()
            level = len(m.group(1))
            path[:] = [(l, h) for l, h in path if l < level] + [(level, m.group(2).strip())]
        else:
            buf.append(line)
    flush()
    return chunks


md = "# Travel\nIntro.\n## Hotels\n### London\nCap is 180 GBP.\n## Flights\nEconomy under 6h."
out = chunk_markdown(md)
assert out == [
    {"headings": "Travel", "text": "Intro."},
    {"headings": "Travel > Hotels > London", "text": "Cap is 180 GBP."},
    {"headings": "Travel > Flights", "text": "Economy under 6h."},
]
```

Why it helps: "Cap is 180 GBP." on its own is ambiguous. With its heading path, both the embedding and the LLM know it is the London hotel cap. Headings also make good citation labels. Long sections still need a secondary size-based split.

## Likely follow-ups

- How would you chunk a PDF that has no reliable heading markup?

---

[← Q0204](../../batch_03_rag_retrieval/0204_recursive_text_splitting/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0206 →](../../batch_03_rag_retrieval/0206_choosing_a_chunk_size/README.md)
