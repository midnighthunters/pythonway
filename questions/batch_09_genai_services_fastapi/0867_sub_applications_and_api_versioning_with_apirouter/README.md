# Q0867 · Sub-applications and API versioning with APIRouter

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Easy |

## Question

Write Python code demonstrating modular API versioning in FastAPI using `APIRouter` to mount `/v1` and `/v2` endpoints with distinct schemas and business logic.

## Answer

Enterprise platforms evolve over years. While `/v1` might return legacy string completions, `/v2` returns structured schema objects with citation metadata. `APIRouter` provides clean separation of concerns.

```python
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

v1_router = APIRouter(prefix="/v1")
v2_router = APIRouter(prefix="/v2")


@v1_router.get("/summary")
def get_summary_v1():
    return {"summary": "Simple text summary"}


@v2_router.get("/summary")
def get_summary_v2():
    return {
        "summary": "Detailed structured summary",
        "citations": ["10-K Item 7", "Press Release"],
        "confidence": 0.98,
    }


app.include_router(v1_router)
app.include_router(v2_router)

client = TestClient(app)

r1 = client.get("/v1/summary")
assert r1.status_code == 200
assert "citations" not in r1.json()

r2 = client.get("/v2/summary")
assert r2.status_code == 200
assert len(r2.json()["citations"]) == 2
```

## Likely follow-ups

- How do you handle schema deprecation warnings in HTTP response headers (`Sunset` / `Deprecation`)?
- What are the trade-offs between URL path versioning (`/v1`) versus header versioning (`Accept: application/vnd.jpmc.v1+json`)?

---

[← Q0866](../../batch_09_genai_services_fastapi/0866_fastapi_dependency_overrides_for_integration_testing/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0868 →](../../batch_09_genai_services_fastapi/0868_mutual_tls_client_certificate_authentication_in_fastapi/README.md)
