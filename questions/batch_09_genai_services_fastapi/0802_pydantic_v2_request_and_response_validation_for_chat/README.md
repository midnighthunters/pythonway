# Q0802 · Pydantic v2 request and response validation for chat endpoints

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Easy |

## Question

Write Python code using Pydantic v2 to validate an incoming chat completion request, enforcing strict role constraints, message history length, and temperature boundaries.

## Answer

```python
from typing import List, Literal, Optional
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage] = Field(min_length=1, max_length=50)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=500, gt=0, le=4096)


app = FastAPI()


@app.post("/chat")
def create_chat(req: ChatCompletionRequest):
    last_msg = req.messages[-1]
    return {
        "reply": f"Echo: {last_msg.content}",
        "role": "assistant",
        "temperature_used": req.temperature,
    }


client = TestClient(app)

# Valid request
valid_payload = {
    "messages": [{"role": "user", "content": "What is VaR?"}],
    "temperature": 0.2,
}
resp = client.post("/chat", json=valid_payload)
assert resp.status_code == 200
assert resp.json()["temperature_used"] == 0.2

# Invalid request: bad role and out-of-range temperature
bad_payload = {
    "messages": [{"role": "admin", "content": ""}],
    "temperature": 3.5,
}
err_resp = client.post("/chat", json=bad_payload)
assert err_resp.status_code == 422
```

## Likely follow-ups

- Why is Pydantic v2 significantly faster than Pydantic v1 for high-throughput GenAI microservices?
- How does `Field(..., extra="forbid")` protect against parameter injection attacks?

---

[← Q0801](../../batch_09_genai_services_fastapi/0801_fastapi_lifespan_context_manager_for_genai_models/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0803 →](../../batch_09_genai_services_fastapi/0803_fastapi_dependency_injection_for_tenant_identification_and/README.md)
