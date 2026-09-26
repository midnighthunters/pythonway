# Q0856 · Structured JSON logging middleware with correlation IDs

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Medium |

## Question

Write Python code implementing a FastAPI Starlette middleware that generates or extracts an `X-Correlation-ID` header, injects it into request state, and logs request lifecycle events in structured JSON format.

## Answer

In distributed microservices, tracing a user's prompt across API Gateways, FastAPI services, vector databases, and model providers requires a consistent correlation ID (or trace ID).

```python
import json
import uuid
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        corr_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        request.state.correlation_id = corr_id

        # Log incoming request
        log_entry = {
            "event": "request_start",
            "correlation_id": corr_id,
            "path": request.url.path,
            "method": request.method,
        }
        # In production: write to stdout / logger
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = corr_id
        return response


app.add_middleware(CorrelationIdMiddleware)


@app.get("/status")
def status_endpoint(request: Request):
    return {"status": "ok", "corr_id": request.state.correlation_id}


client = TestClient(app)

# Request with existing correlation ID
r1 = client.get("/status", headers={"X-Correlation-ID": "trace-xyz-123"})
assert r1.status_code == 200
assert r1.headers["X-Correlation-ID"] == "trace-xyz-123"
assert r1.json()["corr_id"] == "trace-xyz-123"

# Request without correlation ID generates new UUID
r2 = client.get("/status")
assert "X-Correlation-ID" in r2.headers
assert len(r2.headers["X-Correlation-ID"]) > 20
```

## Likely follow-ups

- Why should correlation IDs be propagated across outbound HTTP client requests (e.g. `httpx.AsyncClient`)?
- How do structured JSON logs integrate with Splunk, Datadog, or AWS CloudWatch?

---

[← Q0855](../../batch_09_genai_services_fastapi/0855_measuring_time_to_first_token_and_inter_token_latency_in/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0857 →](../../batch_09_genai_services_fastapi/0857_opentelemetry_instrumentation_for_fastapi_routes_and/README.md)
