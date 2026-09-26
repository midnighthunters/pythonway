# Q0801 · FastAPI lifespan context manager for GenAI models

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Easy |

## Question

Explain the modern FastAPI lifespan context manager (`@asynccontextmanager`) and write Python code that initializes an in-memory embedding model and database pool on startup and closes them on shutdown.

## Answer

In modern FastAPI (replacing deprecated `startup` and `shutdown` event handlers), the `@asynccontextmanager` pattern defines a unified setup and teardown lifecycle for the application.

For GenAI services, preloading embedding models or tokenizer weights into RAM/VRAM during startup avoids cold-start latency penalties on the first user request. Resources yielded into `app.state` are accessible across all route dependencies.

```python
from contextlib import asynccontextmanager
from typing import Dict
from fastapi import FastAPI
from fastapi.testclient import TestClient


class MockEmbeddingModel:
    def __init__(self):
        self.dimension = 384
        self.is_loaded = True

    def embed(self, text: str) -> list:
        return [0.1] * self.dimension


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: preload models and connection pools
    app.state.embedder = MockEmbeddingModel()
    app.state.db_pool = {"status": "connected"}
    yield
    # Shutdown: clean up resources
    app.state.db_pool.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/embed-dim")
def get_dimension():
    return {"dimension": app.state.embedder.dimension}


with TestClient(app) as client:
    response = client.get("/embed-dim")
    assert response.status_code == 200
    assert response.json() == {"dimension": 384}
```

## Likely follow-ups

- What happens if an unhandled exception occurs inside the startup phase of the lifespan generator?
- How does lifespan state differ from request-scoped state?

---

[← Q0800](../../batch_08_azure_openai_bedrock_cloud_ai/0800_comprehensive_end_to_end_integration_test_of_a_multi_cloud/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0802 →](../../batch_09_genai_services_fastapi/0802_pydantic_v2_request_and_response_validation_for_chat/README.md)
