# Q0973 · Evaluating PII redaction precision, recall, and false-positive impact

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Hard |

## Question

Write Python code calculating Precision, Recall, and F1-score for a PII redaction engine against an annotated ground-truth test set, and analyze the trade-off of false positives.

## Answer

In financial services:
- **Low Recall (False Negatives)**: Critical compliance violation! PII leaks into model prompts or third-party cloud logs.
- **Low Precision (False Positives)**: Over-redaction! Benign financial figures (bond yields, stock prices, dates) are erroneously replaced with `[REDACTED_NUMBER]`, destroying the model's ability to analyze financial data.

```python
from typing import List, Set, Tuple


def evaluate_pii_metrics(
    ground_truth_spans: List[Tuple[int, int]],
    predicted_spans: List[Tuple[int, int]],
) -> dict:
    gt_set = set(ground_truth_spans)
    pred_set = set(predicted_spans)

    tp = len(gt_set & pred_set)
    fp = len(pred_set - gt_set)
    fn = len(gt_set - pred_set)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
    }


# Ground truth: 3 PII entities at (0, 10), (20, 30), (50, 60)
gt = [(0, 10), (20, 30), (50, 60)]
# Predicted: matched 2 correctly, 1 false negative, 1 false positive at (70, 80)
pred = [(0, 10), (20, 30), (70, 80)]

metrics = evaluate_pii_metrics(gt, pred)
assert metrics["true_positives"] == 2
assert metrics["false_positives"] == 1
assert metrics["false_negatives"] == 1
assert metrics["recall"] == 0.6667
assert metrics["precision"] == 0.6667
```

## Likely follow-ups

- Why do financial institutions tune PII thresholds for maximum recall ($\beta = 2$ in $F_\beta$ score)?
- How do domain-specific financial dictionaries reduce false positives on ticker symbols and bond CUSIPs?

---

[← Q0972](../../batch_10_ai_security_responsible_ai/0972_audio_transcript_pii_masking_in_call_center_voice_agents/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0974 →](../../batch_10_ai_security_responsible_ai/0974_fast_streaming_pii_redaction_on_token_chunks_without/README.md)
