# Q0361 · Tracing decorator with nested spans

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Observability | Medium |

## Question

Implement a minimal tracing decorator using `contextvars`: each decorated call becomes a span with a parent, duration, attributes and error status, and nesting works across calls (and would across async tasks).

## Answer

```python
import contextvars
import functools
import itertools
import time

_current = contextvars.ContextVar("current_span", default=None)
_ids = itertools.count(1)
SPANS: list[dict] = []


def traced(name: str, **static_attrs):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            span = {"id": next(_ids), "name": name, "parent": _current.get(), "attrs": dict(static_attrs),
                    "status": "ok"}
            token = _current.set(span["id"])
            start = time.perf_counter()
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                span["status"] = f"error:{type(e).__name__}"
                raise
            finally:
                span["duration_ms"] = (time.perf_counter() - start) * 1000
                _current.reset(token)
                SPANS.append(span)
        return wrapper
    return deco


@traced("retrieve", k=5)
def retrieve(q):
    return ["pol-7"]


@traced("llm.chat", model="m1")
def call_llm(prompt):
    if "boom" in prompt:
        raise TimeoutError
    return "180 GBP [1]"


@traced("handle_request")
def handle(q):
    docs = retrieve(q)
    return call_llm(f"{q} {docs}")


assert handle("hotel cap") == "180 GBP [1]"
by_name = {s["name"]: s for s in SPANS}
root = by_name["handle_request"]
assert root["parent"] is None and by_name["retrieve"]["parent"] == root["id"] == by_name["llm.chat"]["parent"]
try:
    handle("boom")
except TimeoutError:
    pass
assert SPANS[-2]["status"] == "error:TimeoutError" and SPANS[-1]["status"] == "error:TimeoutError"
```

`contextvars` is what makes this correct for asyncio, since each task gets its own context copy. In production, use the OpenTelemetry SDK (`tracer.start_as_current_span`) and auto-instrumentation for HTTP and LLM clients. The mechanics are the same.

## Likely follow-ups

- Why would a thread-local fail for asyncio code?

---

[← Q0360](../../batch_04_llm_evaluation_observability/0360_opentelemetry_genai_semantic_conventions/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0362 →](../../batch_04_llm_evaluation_observability/0362_meter_tokens_and_cost_per_tenant/README.md)
