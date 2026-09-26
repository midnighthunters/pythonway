# Q0069 · Concurrency planning with Little's law

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Capacity planning | Easy |

## Question

Use Little's law to estimate concurrent in-flight LLM requests and the number of service replicas needed, given a request rate, average latency, per-replica concurrency limit and headroom.

## Answer

Little's law: L = λ × W. The average number in the system equals the arrival rate times the average time in the system. LLM calls are long (seconds), so concurrency is high even at modest request rates.

```python
import math


def in_flight(rps: float, avg_latency_s: float) -> float:
    return rps * avg_latency_s


def replicas_needed(rps: float, avg_latency_s: float, per_replica: int, headroom: float = 0.3) -> int:
    return math.ceil(in_flight(rps, avg_latency_s) * (1 + headroom) / per_replica)


assert in_flight(20, 8) == 160
assert replicas_needed(20, 8, per_replica=32) == 7
assert replicas_needed(20, 2, per_replica=32) == 2
```

Implications: use async I/O (FastAPI with async HTTP clients) so a replica holds many concurrent streams cheaply, size connection pools to match, and autoscale on concurrency or queue depth rather than CPU, because CPU stays low while waiting on the model.

## Likely follow-ups

- Why is CPU utilisation a poor autoscaling signal for an LLM proxy?

---

[← Q0068](../../batch_01_llm_fundamentals/0068_sustainable_request_rate_from_token_quotas/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0070 →](../../batch_01_llm_fundamentals/0070_data_tensor_and_pipeline_parallelism/README.md)
