# Q0310 · Precision, recall and F1 per label

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Classification metrics | Medium |

## Question

An intent router has five labels with imbalanced traffic. Implement per-label precision, recall and F1, plus macro and micro averages, and explain which average to report.

## Answer

```python
def classification_report(y_true: list[str], y_pred: list[str], labels: list[str]) -> dict:
    per = {}
    for label in labels:
        tp = sum(t == label and p == label for t, p in zip(y_true, y_pred))
        fp = sum(t != label and p == label for t, p in zip(y_true, y_pred))
        fn = sum(t == label and p != label for t, p in zip(y_true, y_pred))
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        per[label] = {"precision": prec, "recall": rec, "f1": f1, "support": tp + fn}
    macro = sum(v["f1"] for v in per.values()) / len(labels)
    micro = sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)
    return {"per_label": per, "macro_f1": macro, "micro_f1": micro}


y_true = ["it"] * 8 + ["hr"] * 2 + ["fraud"]
y_pred = ["it"] * 8 + ["it", "hr"] + ["it"]
r = classification_report(y_true, y_pred, ["it", "hr", "fraud"])
assert r["per_label"]["fraud"]["recall"] == 0.0
assert round(r["micro_f1"], 3) == 0.818 and r["macro_f1"] < 0.6
```

For single-label classification, micro F1 equals accuracy.

Report per-label metrics, and use macro F1 when minority classes matter. Here micro looks fine at 0.82 while the rare but critical "fraud" label has zero recall. Micro averaging hides that.

## Likely follow-ups

- How would you set per-label thresholds when some errors are costlier than others?

---

[← Q0309](../../batch_04_llm_evaluation_observability/0309_semantic_similarity_scoring_and_its_limits/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0311 →](../../batch_04_llm_evaluation_observability/0311_confusion_matrix_for_intent_routing/README.md)
