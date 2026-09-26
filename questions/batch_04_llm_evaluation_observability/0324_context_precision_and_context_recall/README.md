# Q0324 · Context precision and context recall

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | RAG evaluation | Medium |

## Question

Implement context precision (are the relevant retrieved chunks ranked near the top?) and context recall (does the retrieved context cover the facts in the reference answer?).

## Answer

```python
def context_precision(relevance_in_rank_order: list[bool]) -> float:
    hits, total = 0, 0.0
    for k, rel in enumerate(relevance_in_rank_order, start=1):
        if rel:
            hits += 1
            total += hits / k
    return total / hits if hits else 0.0


def context_recall(reference_facts: list[str], supported_by_context: set[str]) -> float:
    if not reference_facts:
        return 1.0
    return sum(f in supported_by_context for f in reference_facts) / len(reference_facts)


assert abs(context_precision([True, False, True]) - (1 + 2 / 3) / 2) < 1e-12
assert context_precision([False, True]) == 0.5
assert context_precision([False, False]) == 0.0
facts = ["cap is 180 GBP", "applies in London", "breakfast included"]
assert abs(context_recall(facts, {"cap is 180 GBP", "applies in London"}) - 2 / 3) < 1e-12
```

These isolate the retrieval stage. Low context recall means the answer can't be complete, however good the model is, so fix retrieval or chunking. Low context precision means noise in the prompt, so improve reranking or reduce k. The relevance and support labels can come from humans, or from an LLM judge validated against humans.

## Likely follow-ups

- Which of these two would you optimise first if answers are often incomplete?

---

[← Q0323](../../batch_04_llm_evaluation_observability/0323_answer_relevance_metric/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0325 →](../../batch_04_llm_evaluation_observability/0325_citation_accuracy_metric/README.md)
