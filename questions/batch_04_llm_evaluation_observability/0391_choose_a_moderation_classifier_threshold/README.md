# Q0391 · Choose a moderation classifier threshold

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Safety evaluation | Medium |

## Question

A classifier scores prompts for policy violations. Given labelled scores, compute precision and recall at candidate thresholds, and pick the highest threshold that still achieves the recall target (to limit false positives).

## Answer

```python
def threshold_table(scores: list[float], labels: list[bool], thresholds: list[float]) -> list[dict]:
    rows = []
    for t in thresholds:
        pred = [s >= t for s in scores]
        tp = sum(p and l for p, l in zip(pred, labels))
        fp = sum(p and not l for p, l in zip(pred, labels))
        fn = sum(not p and l for p, l in zip(pred, labels))
        rows.append({"t": t, "precision": tp / (tp + fp) if tp + fp else 1.0, "recall": tp / (tp + fn) if tp + fn else 1.0})
    return rows


def pick_for_recall(rows: list[dict], min_recall: float) -> float | None:
    ok = [r["t"] for r in rows if r["recall"] >= min_recall]
    return max(ok) if ok else None


scores = [0.95, 0.9, 0.85, 0.7, 0.6, 0.55, 0.4, 0.3, 0.2, 0.1]
labels = [True, True, False, True, True, False, False, True, False, False]
rows = threshold_table(scores, labels, [0.2, 0.3, 0.5, 0.65, 0.8])
assert pick_for_recall(rows, 0.8) == 0.5
assert next(r for r in rows if r["t"] == 0.5)["precision"] == 4 / 6
```

For safety filters, recall is usually the constraint (catch at least 80–95% of violations), and you choose the threshold that minimises false positives subject to it. The false positives aren't free: blocked legitimate users go elsewhere or work around the tool. Re-fit thresholds per language and after classifier updates.

## Likely follow-ups

- Would you use the same threshold for input and output moderation?

---

[← Q0390](../../batch_04_llm_evaluation_observability/0390_counterfactual_name_swap_test/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0392 →](../../batch_04_llm_evaluation_observability/0392_guardrail_false_positives/README.md)
