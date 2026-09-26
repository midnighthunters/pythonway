# Q0805 · Global exception handler for model provider errors

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Medium |

## Question

Write Python code for a FastAPI global exception handler that intercepts third-party cloud AI exceptions (e.g. Azure OpenAI 429 or Bedrock timeouts) and transforms them into standard RFC 7807 Problem Details.

## Answer

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient


class CloudAIProviderException(Exception):
    def __init__(self, provider: str, status_code: int, message: str):
        self.provider = provider
        self.status_code = status_code
        self.message = message


app = FastAPI()


@app.exception_handler(CloudAIProviderException)
async def cloud_ai_exception_handler(request: Request, exc: CloudAIProviderException):
    # Map upstream provider 429/5xx into sanitized client response
    http_status = 503 if exc.status_code in {429, 500, 502, 503, 504} else 500
    problem_details = {
        "type": "https://errors.bank.internal/cloud-ai-provider-error",
        "title": "Upstream Cloud AI Service Degraded",
        "status": http_status,
        "detail": f"Provider '{exc.provider}' encountered transient failure. Request will be retried.",
        "instance": request.url.path,
    }
    return JSONResponse(status_code=http_status, content=problem_details)


@app.get("/trigger-error")
def trigger_error():
    raise CloudAIProviderException(provider="AzureOpenAI", status_code=429, message="Quota limit exceeded")


client = TestClient(app)
res = client.get("/trigger-error")
assert res.status_code == 503
assert res.json()["title"] == "Upstream Cloud AI Service Degraded"
assert "AzureOpenAI" in res.json()["detail"]
```

## Likely follow-ups

- Why should internal raw exception stack traces never be returned to the client in production?
- What RFC 7807 fields provide machine-readable error codes for client SDKs?

---

[← Q0804](../../batch_09_genai_services_fastapi/0804_preventing_event_loop_blocking_in_async_fastapi_routes/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0806 →](../../batch_09_genai_services_fastapi/0806_testing_genai_endpoints_with_fastapi_testclient_and_mocking/README.md)
