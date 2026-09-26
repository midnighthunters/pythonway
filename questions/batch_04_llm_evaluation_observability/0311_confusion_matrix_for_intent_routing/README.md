# Q0311 · Confusion matrix for intent routing

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Classification metrics | Easy |

## Question

Build a confusion matrix from predictions and list the most frequent confusions, to guide prompt or label-definition fixes.

## Answer

```python
from collections import Counter


def confusions(y_true: list[str], y_pred: list[str], top: int = 3) -> tuple[dict, list]:
    matrix = Counter(zip(y_true, y_pred))
    off_diag = sorted(((n, t, p) for (t, p), n in matrix.items() if t != p), reverse=True)[:top]
    return dict(matrix), [(t, p, n) for n, t, p in off_diag]


y_true = ["billing", "billing", "access", "access", "access", "other", "billing"]
y_pred = ["billing", "access", "access", "billing", "billing", "other", "access"]
m, worst = confusions(y_true, y_pred)
assert m[("billing", "access")] == 2 and m[("access", "billing")] == 2
assert worst[0][2] == 2
```

The top confusions tell you where the label definitions overlap, for example billing versus access for "can't log in to pay my bill". Fix it with clearer boundary rules in the prompt, a new label, or a clarifying question, then re-measure.

## Likely follow-ups

- When is a frequent confusion a sign that the labels themselves are wrong?

---

[← Q0310](../../batch_04_llm_evaluation_observability/0310_precision_recall_and_f1_per_label/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0312 →](../../batch_04_llm_evaluation_observability/0312_cohen_s_kappa_for_annotator_agreement/README.md)
