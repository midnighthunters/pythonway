# Q0203 · Fixed-size chunking with overlap

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Chunking | Easy |

## Question

Implement word-based fixed-size chunking with overlap, and explain why overlap helps and what it costs.

## Answer

```python
def chunk_words(text: str, size: int, overlap: int) -> list[str]:
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("need size > 0 and 0 <= overlap < size")
    words, step, chunks = text.split(), size - overlap, []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
    return chunks


text = " ".join(f"w{i}" for i in range(10))
assert chunk_words(text, 4, 1) == ["w0 w1 w2 w3", "w3 w4 w5 w6", "w6 w7 w8 w9"]
assert chunk_words(text, 20, 5) == [text]
assert chunk_words("", 4, 1) == []
```

Overlap keeps a sentence that straddles a boundary retrievable from at least one chunk, and gives each chunk some local context. It costs index size, embedding spend and duplicate hits (the same passage appearing twice in the top k). 10–20% overlap is a common start.

Production chunkers count model tokens, not words, and respect sentence and structure boundaries.

## Likely follow-ups

- How would you deduplicate overlapping hits before building the prompt?

---

[← Q0202](../../batch_03_rag_retrieval/0202_when_not_to_use_rag/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0204 →](../../batch_03_rag_retrieval/0204_recursive_text_splitting/README.md)
