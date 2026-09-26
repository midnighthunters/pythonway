# Q0238 · Build numbered context with a citation map

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Citations | Medium |

## Question

Build the prompt's source block with numbered entries, and a citation map from each number to the document id, title, URL and page. Then resolve the citations in an answer into links, rejecting unknown numbers.

## Answer

```python
import re


def build_sources(chunks: list[dict]) -> tuple[str, dict[int, dict]]:
    blocks, cmap = [], {}
    for i, c in enumerate(chunks, start=1):
        cmap[i] = {k: c[k] for k in ("doc_id", "title", "url", "page")}
        blocks.append(f"[{i}] {c['title']} (p. {c['page']})\n{c['text']}")
    return "\n\n".join(blocks), cmap


def resolve_citations(answer: str, cmap: dict[int, dict]) -> tuple[list[dict], list[int]]:
    nums = list(dict.fromkeys(int(n) for n in re.findall(r"\[(\d+)\]", answer)))
    return [cmap[n] for n in nums if n in cmap], [n for n in nums if n not in cmap]


chunks = [{"doc_id": "pol-7", "title": "Travel Policy", "url": "https://intranet.example/pol-7", "page": 4,
           "text": "London hotels capped at 180 GBP."},
          {"doc_id": "faq-2", "title": "Expenses FAQ", "url": "https://intranet.example/faq-2", "page": 1,
           "text": "File claims within 30 days."}]
text, cmap = build_sources(chunks)
assert text.startswith("[1] Travel Policy (p. 4)\nLondon hotels")
links, bad = resolve_citations("Cap is 180 GBP [1]; claims within 30 days [2][1]. See also [5].", cmap)
assert [l["doc_id"] for l in links] == ["pol-7", "faq-2"] and bad == [5]
```

Short numeric ids ([1], [2]) are easier for models to use correctly than long document ids. Keep the map server-side and render proper links in the UI, so you never trust a model-generated URL.

## Likely follow-ups

- Why should the UI never render URLs the model wrote itself?

---

[← Q0237](../../batch_03_rag_retrieval/0237_tenant_isolation_in_vector_stores/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0239 →](../../batch_03_rag_retrieval/0239_pack_context_under_a_token_budget/README.md)
