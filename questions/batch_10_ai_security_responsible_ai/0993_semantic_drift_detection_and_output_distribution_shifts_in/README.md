# Q0993 · Semantic drift detection and output distribution shifts in production

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Medium |

## Question

Explain semantic drift in production GenAI models, and write Python code implementing Population Stability Index (PSI) or embedding centroid drift calculation.

## Answer

Over months, user queries and model outputs shift due to changing macroeconomic conditions (e.g. from low interest rate queries to high inflation queries) or silent upstream model checkpoint updates.

Calculating the distance between the **baseline embedding centroid** and the **current production embedding centroid** detects semantic drift.

```python
import math
from typing import List


def calculate_centroid(vectors: List[List[float]]) -> List[float]:
    dim = len(vectors[0])
    centroid = [0.0] * dim
    for v in vectors:
        for i in range(dim):
            centroid[i] += v[i]
    return [c / len(vectors) for c in centroid]


def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


class SemanticDriftDetector:
    def __init__(self, baseline_vectors: List[List[float]], drift_threshold: float = 0.25):
        self.baseline_centroid = calculate_centroid(baseline_vectors)
        self.threshold = drift_threshold

    def evaluate_production_batch(self, batch_vectors: List[List[float]]) -> dict:
        current_centroid = calculate_centroid(batch_vectors)
        drift_dist = euclidean_distance(self.baseline_centroid, current_centroid)
        is_drifted = drift_dist > self.threshold
        return {
            "drift_distance": round(drift_dist, 4),
            "drift_detected": is_drifted,
        }


# Baseline queries centered around [0.1, 0.1]
baseline = [[0.1, 0.1], [0.12, 0.08], [0.09, 0.11]]
detector = SemanticDriftDetector(baseline, drift_threshold=0.20)

# Stable production batch
stable_batch = [[0.11, 0.10], [0.09, 0.12]]
assert detector.evaluate_production_batch(stable_batch)["drift_detected"] is False

# Drifted production batch centered around [0.8, 0.8]
drifted_batch = [[0.8, 0.85], [0.82, 0.78]]
assert detector.evaluate_production_batch(drifted_batch)["drift_detected"] is True
```

## Likely follow-ups

- What is Population Stability Index (PSI) and how is it adapted for discrete token distributions?
- What automated alerts should notify model validation teams when semantic drift exceeds 0.25?

---

[← Q0992](../../batch_10_ai_security_responsible_ai/0992_llm_as_a_judge_designing_reliable_evaluation_rubrics_and/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0994 →](../../batch_10_ai_security_responsible_ai/0994_shadow_deployments_and_champion_challenger_routing_in_live/README.md)
