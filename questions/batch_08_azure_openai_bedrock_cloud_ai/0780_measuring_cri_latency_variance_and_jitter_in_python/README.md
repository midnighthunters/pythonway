# Q0780 · Measuring CRI latency variance and jitter in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Write Python code that calculates the mean, P95, and jitter (standard deviation) of invocation latencies across multiple simulated cloud serving regions.

## Answer

```python
import math
import statistics
from typing import Dict, List


def compute_regional_latency_metrics(samples: List[float]) -> Dict[str, float]:
    if not samples:
        return {"mean": 0.0, "p95": 0.0, "jitter": 0.0}

    mean_val = statistics.mean(samples)
    stdev_val = statistics.stdev(samples) if len(samples) > 1 else 0.0

    sorted_samples = sorted(samples)
    p95_idx = int(0.95 * len(sorted_samples))
    p95_val = sorted_samples[min(p95_idx, len(sorted_samples) - 1)]

    return {
        "mean_ms": round(mean_val, 2),
        "p95_ms": round(p95_val, 2),
        "jitter_ms": round(stdev_val, 2),
    }


latencies = [120.0, 135.0, 125.0, 140.0, 310.0, 122.0, 128.0, 130.0, 124.0, 131.0]
stats = compute_regional_latency_metrics(latencies)

assert stats["mean_ms"] > 130.0
assert stats["p95_ms"] == 310.0
assert stats["jitter_ms"] > 0.0
```

## Likely follow-ups

- Why does standard deviation serve as an effective proxy for network jitter in streaming APIs?
- How can outliers (like the 310ms latency spike) be isolated in observability dashboards?

---

[← Q0779](../../batch_08_azure_openai_bedrock_cloud_ai/0779_cross_region_inference_profile_latency_monitoring/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0781 →](../../batch_08_azure_openai_bedrock_cloud_ai/0781_dual_cloud_ai_gateway_architecture_azure_plus_aws_active/README.md)
