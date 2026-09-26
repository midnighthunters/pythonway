# Q0804 · Preventing event loop blocking in async FastAPI routes

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Medium |

## Question

Why will running CPU-intensive operations (like tokenization or vector distance math) inside an `async def` route freeze the entire FastAPI server? How does `asyncio.to_thread` fix this?

## Answer

Python's `asyncio` uses a single-threaded cooperative event loop. When a route is declared `async def`, FastAPI executes it directly on the main event loop thread:
- If an `async def` endpoint performs heavy synchronous CPU work (e.g. running BPE tokenization on a 50-page text, computing matrix multiplication with NumPy, or making a synchronous `requests.get()` call), the entire event loop is blocked.
- While blocked, the server cannot accept new TCP connections, serve other active requests, or stream SSE chunks to connected users.

Solutions:
1. Standard `def` route: If declared as `def route()`, FastAPI automatically runs it in an external thread pool (ThreadPoolExecutor) managed by AnyIO.
2. `asyncio.to_thread`: Inside an `async def` function, wrap heavy CPU tasks with `await asyncio.to_thread(cpu_heavy_func, *args)`.

```python
import asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient


def compute_cpu_heavy_dot_product(vec_a: list, vec_b: list) -> float:
    # Synchronous CPU-bound computation
    return sum(x * y for x, y in zip(vec_a, vec_b))


app = FastAPI()


@app.post("/similarity")
async def calculate_similarity(payload: dict):
    vec_a = payload.get("a", [1.0, 2.0])
    vec_b = payload.get("b", [3.0, 4.0])

    # Offload CPU execution to worker thread pool
    score = await asyncio.to_thread(compute_cpu_heavy_dot_product, vec_a, vec_b)
    return {"dot_product": score}


client = TestClient(app)
res = client.post("/similarity", json={"a": [1.0, 2.0], "b": [3.0, 4.0]})
assert res.status_code == 200
assert res.json()["dot_product"] == 11.0
```

## Likely follow-ups

- What is the default maximum worker thread limit in AnyIO / Starlette?
- Why should GPU inference never be invoked synchronously on the main asyncio thread?

---

[← Q0803](../../batch_09_genai_services_fastapi/0803_fastapi_dependency_injection_for_tenant_identification_and/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0805 →](../../batch_09_genai_services_fastapi/0805_global_exception_handler_for_model_provider_errors/README.md)
