# Q0732 · Implementing a queue-depth autoscaling simulator in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Elastic Compute | Hard |

## Question

Write Python code that simulates a KEDA-style autoscaler, computing desired replica counts from queue depth and enforcing minimum, maximum, and cooldown limits.

## Answer

```python
import math
from typing import Dict


class QueueAutoscaler:
    def __init__(self, min_replicas: int, max_replicas: int, target_queue_per_pod: int):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.target_queue_per_pod = target_queue_per_pod
        self.current_replicas = min_replicas

    def compute_desired_replicas(self, total_queued_requests: int) -> int:
        if total_queued_requests <= 0:
            desired = self.min_replicas
        else:
            # Scale based on queue depth target
            desired = math.ceil(total_queued_requests / self.target_queue_per_pod)

        # Enforce boundaries
        desired = max(self.min_replicas, min(self.max_replicas, desired))
        self.current_replicas = desired
        return desired


scaler = QueueAutoscaler(min_replicas=2, max_replicas=10, target_queue_per_pod=5)

# Idle: minimum replicas
assert scaler.compute_desired_replicas(0) == 2

# Moderate load: 15 queued requests / 5 target = 3 pods
assert scaler.compute_desired_replicas(15) == 3

# High spike: 100 queued requests capped at max 10 pods
assert scaler.compute_desired_replicas(100) == 10
```

## Likely follow-ups

- How does scale-down stabilization prevent pod flapping during fluctuating traffic?
- What metrics beyond queue depth should influence scaling decisions?

---

[← Q0731](../../batch_08_azure_openai_bedrock_cloud_ai/0731_autoscaling_inference_pods_with_keda_based_on_queue_depth/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0733 →](../../batch_08_azure_openai_bedrock_cloud_ai/0733_spot_instances_for_batch_offline_llm_inference/README.md)
