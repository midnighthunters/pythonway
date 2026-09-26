# Q0082 · Expected calibration error

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Model confidence | Medium |

## Question

Implement expected calibration error (ECE) for predicted confidences and correctness labels, and explain why calibration matters for routing to human review.

## Answer

Bucket predictions by confidence. ECE is the weighted average gap between mean confidence and actual accuracy per bucket. A calibrated model that says 0.8 is right 80% of the time.

```python
import numpy as np


def expected_calibration_error(conf, correct, n_bins: int = 10) -> float:
    conf = np.asarray(conf, dtype=float)
    correct = np.asarray(correct, dtype=float)
    bins = np.minimum((conf * n_bins).astype(int), n_bins - 1)
    ece = 0.0
    for b in range(n_bins):
        m = bins == b
        if m.any():
            ece += m.mean() * abs(conf[m].mean() - correct[m].mean())
    return float(ece)


assert np.isclose(expected_calibration_error([0.8] * 10, [1] * 8 + [0] * 2), 0.0)
assert np.isclose(expected_calibration_error([0.9] * 10, [1] * 5 + [0] * 5), 0.4)
```

Why it matters: thresholds such as "auto-approve above 0.9, send the rest to an analyst" only work if 0.9 means what it says. LLM-reported confidences and even logprobs are often miscalibrated. Fix them with temperature scaling or isotonic regression fitted on labelled data, and re-check after model upgrades.

## Likely follow-ups

- How many labelled examples do you need for a trustworthy reliability diagram?

---

[← Q0081](../../batch_01_llm_fundamentals/0081_unicode_normalisation_before_model_input/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0083 →](../../batch_01_llm_fundamentals/0083_logit_bias_to_ban_or_force_tokens/README.md)
