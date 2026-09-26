# Q0674 · Tracing multi-agent A2A message chains with correlation IDs

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A orchestration | Medium |

## Question

Write Python code that injects and extracts distributed correlation IDs into A2A task headers for logging and observability.

## Answer

```python
import uuid
from typing import Any, Dict, Optional


class A2ATracingInterceptor:
    CORRELATION_HEADER = "X-Correlation-ID"

    @classmethod
    def inject_headers(cls, headers: Dict[str, str], correlation_id: Optional[str] = None) -> Dict[str, str]:
        new_headers = dict(headers)
        new_headers[cls.CORRELATION_HEADER] = correlation_id or f"corr-{uuid.uuid4().hex[:12]}"
        return new_headers

    @classmethod
    def extract_or_generate(cls, headers: Dict[str, str]) -> str:
        return headers.get(cls.CORRELATION_HEADER, f"corr-{uuid.uuid4().hex[:12]}")


h = A2ATracingInterceptor.inject_headers({"Authorization": "Bearer token"}, correlation_id="corr-test-123")
assert h["X-Correlation-ID"] == "corr-test-123"

extracted = A2ATracingInterceptor.extract_or_generate(h)
assert extracted == "corr-test-123"
```

## Likely follow-ups

- How does correlation ID propagation tie into OpenTelemetry and Jaeger tracing?
- Why is an end-to-end trace ID critical when investigating trade break resolution failures?

---

[← Q0673](../../batch_07_mcp_a2a_skills_assistants/0673_error_handling_and_failover_in_a2a_worker_pools/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0675 →](../../batch_07_mcp_a2a_skills_assistants/0675_evaluating_performance_and_communication_cost_in_a2a_swarms/README.md)
