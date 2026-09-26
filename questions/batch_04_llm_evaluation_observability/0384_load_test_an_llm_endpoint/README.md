# Q0384 · Load test an LLM endpoint

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Performance testing | Medium |

## Question

Write an async load generator that sends N requests at a fixed concurrency to an endpoint, and reports throughput and latency percentiles. Test it against a fake endpoint with known latency.

## Answer

```python
import asyncio
import math
import time
from typing import Awaitable, Callable


async def load_test(call: Callable[[int], Awaitable[None]], n: int, concurrency: int) -> dict:
    sem = asyncio.Semaphore(concurrency)
    latencies: list[float] = []
    errors = 0

    async def one(i: int) -> None:
        nonlocal errors
        async with sem:
            start = time.perf_counter()
            try:
                await call(i)
                latencies.append(time.perf_counter() - start)
            except Exception:
                errors += 1

    t0 = time.perf_counter()
    await asyncio.gather(*(one(i) for i in range(n)))
    elapsed = time.perf_counter() - t0
    s = sorted(latencies)
    pct = lambda p: s[max(0, math.ceil(p * len(s)) - 1)] if s else None
    return {"throughput_rps": n / elapsed, "p50_s": pct(0.5), "p95_s": pct(0.95), "errors": errors}


async def fake_endpoint(i: int) -> None:
    await asyncio.sleep(0.02)
    if i % 50 == 49:
        raise RuntimeError("429")


r = asyncio.run(load_test(fake_endpoint, n=100, concurrency=10))
assert r["errors"] == 2 and 0.015 < r["p50_s"] < 0.2
assert r["throughput_rps"] > 100
```

With ten concurrent 20 ms calls, throughput is well above 100 requests per second. For real LLM endpoints, also measure TTFT and tokens per second under streaming, use realistic prompt and output lengths (they dominate latency), respect provider quotas (test against a dedicated deployment), and ramp load gradually to find the knee where latency explodes.

## Likely follow-ups

- Why must load tests use realistic prompt lengths rather than "hello"?

---

[← Q0383](../../batch_04_llm_evaluation_observability/0383_error_analysis_workflow/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0385 →](../../batch_04_llm_evaluation_observability/0385_rate_limit_evaluation_traffic_with_a_token_bucket/README.md)
