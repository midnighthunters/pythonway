# Q0857 · OpenTelemetry instrumentation for FastAPI routes and downstream model calls

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Hard |

## Question

Explain how OpenTelemetry (OTel) traces span across FastAPI route handlers and downstream model API calls, and write Python code simulating nested trace span creation.

## Answer

OpenTelemetry provides vendor-neutral distributed tracing. A root span is created for the HTTP request, and child spans wrap vector database similarity queries and LLM provider invocations, measuring duration and capturing metadata (tokens, model name, status code).

```python
import time
from typing import Any, Dict, List, Optional


class MockSpan:
    def __init__(self, name: str, parent: Optional["MockSpan"] = None):
        self.name = name
        self.parent = parent
        self.attributes: Dict[str, Any] = {}
        self.start_time = time.time()
        self.end_time = None

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def finish(self) -> None:
        self.end_time = time.time()


class MockTracer:
    def __init__(self):
        self.spans: List[MockSpan] = []

    def start_span(self, name: str, parent: Optional[MockSpan] = None) -> MockSpan:
        span = MockSpan(name, parent)
        self.spans.append(span)
        return span


tracer = MockTracer()

# Simulate FastAPI Request Trace
root_span = tracer.start_span("HTTP POST /chat")
root_span.set_attribute("http.method", "POST")

# Child Span 1: Vector DB query
span_vdb = tracer.start_span("pgvector.similarity_search", parent=root_span)
span_vdb.set_attribute("db.top_k", 5)
span_vdb.finish()

# Child Span 2: Downstream LLM call
span_llm = tracer.start_span("openai.chat_completions", parent=root_span)
span_llm.set_attribute("gen_ai.model", "gpt-4o")
span_llm.set_attribute("gen_ai.usage.prompt_tokens", 450)
span_llm.finish()

root_span.finish()

assert len(tracer.spans) == 3
assert span_vdb.parent == root_span
assert span_llm.attributes["gen_ai.model"] == "gpt-4o"
```

## Likely follow-ups

- What are the standard OpenTelemetry semantic conventions for Generative AI (`gen_ai.system`, `gen_ai.usage`)?
- How do you avoid tracing sensitive user PII into span attributes?

---

[← Q0856](../../batch_09_genai_services_fastapi/0856_structured_json_logging_middleware_with_correlation_ids/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0858 →](../../batch_09_genai_services_fastapi/0858_prometheus_metrics_endpoint_for_request_counts_latencies/README.md)
