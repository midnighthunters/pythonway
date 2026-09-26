# Q0844 · Per-request token budgeting and hard cutoff limits in FastAPI

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Easy |

## Question

Write Python code using FastAPI middleware or dependency injection to inspect and enforce request token budgets, rejecting requests exceeding max allowed input tokens with HTTP 413.

## Answer

Allowing users to upload 100,000-token documents to un-budgeted chat routes can exhaust server memory, cause client timeouts, and trigger multi-dollar single-request API charges. Enforcing strict input limits safeguards the microservice.

```python
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


class ChatPayload(BaseModel):
    prompt: str = Field(min_length=1)
    max_tokens: int = Field(default=256)


app = FastAPI()

MAX_ALLOWED_INPUT_CHARS = 4000  # Rough token budget safeguard


@app.post("/generate")
def generate_text(payload: ChatPayload):
    if len(payload.prompt) > MAX_ALLOWED_INPUT_CHARS:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Prompt exceeds max character limit of {MAX_ALLOWED_INPUT_CHARS}",
        )
    return {"status": "accepted", "length": len(payload.prompt)}


client = TestClient(app)

# Allowed request
res = client.post("/generate", json={"prompt": "Short market query"})
assert res.status_code == 200

# Exceeded budget
huge_prompt = "A" * 5000
res_huge = client.post("/generate", json={"prompt": huge_prompt})
assert res_huge.status_code == 413
assert "exceeds max character limit" in res_huge.json()["detail"]
```

## Likely follow-ups

- Why is character count an approximation of token count, and when should you use `tiktoken` directly?
- How does token truncation middleware differ from hard HTTP 413 rejections?

---

[← Q0843](../../batch_09_genai_services_fastapi/0843_tenant_based_quota_enforcement_and_tiered_subscription_rate/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0845 →](../../batch_09_genai_services_fastapi/0845_finops_cost_metering_calculating_usd_cost_per_request_by/README.md)
