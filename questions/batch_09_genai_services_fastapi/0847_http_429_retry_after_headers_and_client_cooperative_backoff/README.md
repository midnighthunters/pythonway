# Q0847 · HTTP 429 Retry-After headers and client cooperative backoff

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Easy |

## Question

Write Python code returning an HTTP 429 Too Many Requests response with standard `Retry-After` headers and compliant error schema.

## Answer

When rate limits are breached, standard RFC 6585 compliance requires returning HTTP 429 with a `Retry-After` header indicating the number of seconds the client must wait before retrying.

```python
from fastapi import FastAPI, Response, status
from fastapi.testclient import TestClient

app = FastAPI()

CALL_COUNT = 0


@app.get("/rate-limited-endpoint")
def sensitive_endpoint(response: Response):
    global CALL_COUNT
    CALL_COUNT += 1
    if CALL_COUNT > 1:
        # Rate limit breached: return 429 with Retry-After header
        response.status_code = status.HTTP_429_TOO_MANY_REQUESTS
        response.headers["Retry-After"] = "15"  # Wait 15 seconds
        response.headers["X-RateLimit-Limit"] = "1"
        return {"error": "Too Many Requests", "retry_after_seconds": 15}
    return {"status": "success"}


client = TestClient(app)
r1 = client.get("/rate-limited-endpoint")
assert r1.status_code == 200

r2 = client.get("/rate-limited-endpoint")
assert r2.status_code == 429
assert r2.headers["Retry-After"] == "15"
assert r2.json()["retry_after_seconds"] == 15
```

## Likely follow-ups

- How does exponential backoff with full jitter protect downstream servers from herd retries?
- Can `Retry-After` be specified as an HTTP-date format instead of integer seconds?

---

[← Q0846](../../batch_09_genai_services_fastapi/0846_asynchronous_usage_event_publishing_to_kafka_for_enterprise/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0848 →](../../batch_09_genai_services_fastapi/0848_concurrency_limiting_with_asyncio_semaphore_to_prevent/README.md)
