# Q0363 · Structured JSON logs for LLM calls

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Observability | Easy |

## Question

Write a structured logger for LLM calls that emits one JSON line with a fixed schema, drops fields that aren't on an allowlist (so prompts and secrets aren't logged by accident), and includes the trace id.

## Answer

```python
import json
from datetime import datetime, timezone

ALLOWED = {"trace_id", "tenant", "assistant", "model", "prompt_version", "input_tokens", "output_tokens",
           "latency_ms", "ttft_ms", "finish_reason", "status", "cache_hit"}


def log_llm_call(**fields) -> str:
    record = {k: v for k, v in fields.items() if k in ALLOWED}
    dropped = sorted(set(fields) - ALLOWED)
    record["ts"] = datetime(2026, 9, 26, 12, 0, tzinfo=timezone.utc).isoformat()
    record["event"] = "llm_call"
    if dropped:
        record["dropped_fields"] = dropped
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


line = log_llm_call(trace_id="t-1", tenant="treasury", model="m1", input_tokens=900, output_tokens=120,
                    finish_reason="stop", prompt="What is my salary?", api_key="sk-live-123")
rec = json.loads(line)
assert rec["dropped_fields"] == ["api_key", "prompt"] and "sk-live" not in line and "salary" not in line
assert rec["event"] == "llm_call" and rec["trace_id"] == "t-1"
```

The timestamp is fixed here to keep the test deterministic. Real code uses the current time. An allowlist is safer than a denylist, because new sensitive fields are excluded by default. Recording which fields were dropped helps you notice misuse without logging the values.

## Likely follow-ups

- Where should full prompt content go if investigators need it?

---

[← Q0362](../../batch_04_llm_evaluation_observability/0362_meter_tokens_and_cost_per_tenant/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0364 →](../../batch_04_llm_evaluation_observability/0364_redact_pii_before_logging/README.md)
