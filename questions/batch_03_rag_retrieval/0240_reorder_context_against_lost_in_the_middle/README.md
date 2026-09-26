# Q0240 · Reorder context against lost in the middle

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Context assembly | Easy |

## Question

Models use information at the start and end of long contexts more reliably than in the middle. Implement a reordering that puts the most relevant chunks at the edges and the least relevant in the middle.

## Answer

```python
def reorder_for_edges(items_best_first: list) -> list:
    front, back = [], []
    for i, item in enumerate(items_best_first):
        (front if i % 2 == 0 else back).append(item)
    return front + back[::-1]


assert reorder_for_edges([1, 2, 3, 4, 5]) == [1, 3, 5, 4, 2]
assert reorder_for_edges([1, 2]) == [1, 2]
assert reorder_for_edges([]) == []
```

Rank 1 is first and rank 2 is last, with the weakest in the middle. LangChain ships this as `LongContextReorder`.

The effect varies by model and is smaller in newer long-context models, so verify it on your evaluation set. When chunks from the same document need to be read in order, keep them adjacent and in document order instead.

## Likely follow-ups

- When is document order more important than relevance order?

---

[← Q0239](../../batch_03_rag_retrieval/0239_pack_context_under_a_token_budget/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0241 →](../../batch_03_rag_retrieval/0241_rag_answer_prompt_builder/README.md)
