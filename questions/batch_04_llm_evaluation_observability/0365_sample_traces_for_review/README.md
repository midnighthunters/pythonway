# Q0365 · Sample traces for review

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Observability | Medium |

## Question

You can only review about 1% of traces. Implement a sampler that always keeps errors, negative feedback and guardrail triggers, and deterministically samples the rest by hashing the trace id, so every service makes the same decision for a trace.

## Answer

```python
import hashlib


def keep_trace(trace: dict, rate: float) -> tuple[bool, str]:
    if trace.get("status") == "error":
        return True, "error"
    if trace.get("feedback") == "negative":
        return True, "negative_feedback"
    if trace.get("guardrail_triggered"):
        return True, "guardrail"
    bucket = int(hashlib.sha256(trace["trace_id"].encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
    return (bucket < rate, "sampled") if bucket < rate else (False, "dropped")


traces = [{"trace_id": f"t{i}", "status": "ok"} for i in range(10_000)]
kept = sum(keep_trace(t, 0.01)[0] for t in traces)
assert 70 <= kept <= 130
assert keep_trace({"trace_id": "x", "status": "error"}, 0.0) == (True, "error")
assert keep_trace({"trace_id": "t42", "status": "ok"}, 0.01) == keep_trace({"trace_id": "t42", "status": "ok"}, 0.01)
```

Hash-based head sampling is consistent across services without coordination. Tail-based sampling (decide after the trace completes, so slow or failed traces are kept) needs a collector that buffers spans, which OpenTelemetry collectors support. Stratify the random sample by assistant and language, so small segments still get reviewed.

## Likely follow-ups

- Why is tail-based sampling better for catching slow requests?

---

[← Q0364](../../batch_04_llm_evaluation_observability/0364_redact_pii_before_logging/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0366 →](../../batch_04_llm_evaluation_observability/0366_langsmith_for_tracing_and_evaluation/README.md)
