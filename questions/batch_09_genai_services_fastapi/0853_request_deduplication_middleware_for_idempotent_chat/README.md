# Q0853 · Request deduplication middleware for idempotent chat completions

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Medium |

## Question

Write Python code implementing an in-memory idempotency deduplicator in FastAPI using an `Idempotency-Key` header, preventing duplicate LLM executions when network timeouts cause client retries.

## Answer

If a mobile client or frontend drops connection before receiving an LLM response, it may retry the request with the same `Idempotency-Key`. Without deduplication, the server executes two full model inferences, doubling billing costs and generating duplicate database entries.

```python
from typing import Dict, Optional
from fastapi import FastAPI, Header, HTTPException, Response, status
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()

# Cache mapping: idempotency_key -> response_data
IDEMPOTENCY_STORE: Dict[str, dict] = {}
EXECUTION_COUNT = 0


class ChatRequest(BaseModel):
    prompt: str


@app.post("/chat/completions")
def chat_endpoint(req: ChatRequest, idempotency_key: Optional[str] = Header(None)):
    global EXECUTION_COUNT
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Missing Idempotency-Key header")

    if idempotency_key in IDEMPOTENCY_STORE:
        # Return cached response without re-executing LLM
        return IDEMPOTENCY_STORE[idempotency_key]

    # Execute LLM inference
    EXECUTION_COUNT += 1
    resp_data = {"reply": f"Processed: {req.prompt}", "execution_id": EXECUTION_COUNT}
    IDEMPOTENCY_STORE[idempotency_key] = resp_data
    return resp_data


client = TestClient(app)

# First request
r1 = client.post("/chat/completions", json={"prompt": "Quote AAPL"}, headers={"Idempotency-Key": "idemp-001"})
assert r1.status_code == 200
assert r1.json()["execution_id"] == 1

# Duplicate retry with same key
r2 = client.post("/chat/completions", json={"prompt": "Quote AAPL"}, headers={"Idempotency-Key": "idemp-001"})
assert r2.status_code == 200
assert r2.json()["execution_id"] == 1  # Not re-executed!
assert EXECUTION_COUNT == 1
```

## Likely follow-ups

- What should the middleware do if a duplicate request arrives while the first request is still in-flight?
- How long should idempotency keys be retained in Redis (standard TTL: 24 to 48 hours)?

---

[← Q0852](../../batch_09_genai_services_fastapi/0852_graceful_degradation_and_fallback_to_smaller_models_under/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0854 →](../../batch_09_genai_services_fastapi/0854_streaming_backpressure_handling_when_slow_clients_cannot/README.md)
