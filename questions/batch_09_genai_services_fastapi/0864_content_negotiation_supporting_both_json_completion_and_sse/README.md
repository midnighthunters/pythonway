# Q0864 · Content negotiation supporting both JSON completion and SSE streaming

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Medium |

## Question

Write Python code implementing content negotiation in a single FastAPI route, returning full JSON when `Accept: application/json` is requested and SSE streaming when `Accept: text/event-stream` is requested.

## Answer

A single `/chat/completions` endpoint can serve both batch/scripting clients (who prefer a single JSON response) and interactive web applications (who require token-by-token streaming).

```python
from typing import AsyncGenerator
from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class ChatReq(BaseModel):
    prompt: str


async def token_generator(prompt: str) -> AsyncGenerator[str, None]:
    for word in prompt.split():
        yield f"data: {word}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/chat")
async def unified_chat(req: ChatReq, accept: str = Header(default="application/json")):
    if "text/event-stream" in accept:
        return StreamingResponse(token_generator(req.prompt), media_type="text/event-stream")
    else:
        # Standard JSON response
        return JSONResponse({"reply": f"Answer to: {req.prompt}", "streamed": False})


client = TestClient(app)

# JSON request
r_json = client.post("/chat", json={"prompt": "Hello world"}, headers={"Accept": "application/json"})
assert r_json.status_code == 200
assert r_json.json()["streamed"] is False

# SSE streaming request
r_sse = client.post("/chat", json={"prompt": "Hello world"}, headers={"Accept": "text/event-stream"})
assert r_sse.status_code == 200
assert "text/event-stream" in r_sse.headers["content-type"]
assert "data: Hello" in r_sse.text
```

## Likely follow-ups

- How does the OpenAI specification use the `"stream": true` JSON field versus HTTP `Accept` headers?
- What are the caching implications of serving multiple representations from the same URI?

---

[← Q0863](../../batch_09_genai_services_fastapi/0863_multipart_form_data_with_file_parsing_and_simultaneous_json/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0865 →](../../batch_09_genai_services_fastapi/0865_asynchronous_generator_cancellation_and_memory_cleanup_on/README.md)
