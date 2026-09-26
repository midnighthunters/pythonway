# Q0358 · Detect embedding drift

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Monitoring | Medium |

## Question

Implement a simple embedding-drift monitor: compare the centroid of this week's query embeddings with a reference window, and alert when the cosine distance exceeds a threshold calibrated on normal week-to-week variation.

## Answer

```python
import numpy as np


def centroid_distance(ref: np.ndarray, cur: np.ndarray) -> float:
    a, b = ref.mean(axis=0), cur.mean(axis=0)
    return float(1 - a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def calibrate_threshold(weeks: list[np.ndarray], k: float = 3.0) -> float:
    d = [centroid_distance(weeks[i], weeks[i + 1]) for i in range(len(weeks) - 1)]
    return float(np.mean(d) + k * np.std(d))


rng = np.random.default_rng(0)
topic = rng.normal(size=64)
normal_weeks = [topic + rng.normal(scale=1.0, size=(500, 64)) for _ in range(6)]
threshold = calibrate_threshold(normal_weeks)
new_topic = rng.normal(size=64)
drifted = 0.5 * topic + 0.8 * new_topic + rng.normal(scale=1.0, size=(500, 64))
assert centroid_distance(normal_weeks[-1], topic + rng.normal(size=(500, 64))) < threshold
assert centroid_distance(normal_weeks[-1], drifted) > threshold
```

Centroid distance is crude (it can miss a new cluster that's a small fraction of traffic). Complement it with clustering new queries and checking cluster sizes, or with a maximum mean discrepancy test. When drift fires, sample the new cluster's queries, label them, and extend the evaluation set.

## Likely follow-ups

- How would you detect a small new cluster that centroid distance misses?

---

[← Q0357](../../batch_04_llm_evaluation_observability/0357_detect_query_drift_with_psi/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0359 →](../../batch_04_llm_evaluation_observability/0359_traces_spans_and_attributes_for_llm_apps/README.md)
