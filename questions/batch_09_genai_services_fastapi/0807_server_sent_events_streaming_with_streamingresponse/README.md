# Q0807 · Server-Sent Events streaming with StreamingResponse

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI streaming | Medium |

## Question

Write Python code for a FastAPI endpoint that streams real-time LLM token chunks to a client using `StreamingResponse` and Server-Sent Events (SSE).

## Answer

Server-Sent Events (SSE) provide a lightweight, unidirectional HTTP streaming transport. The server sets `media_type="text/event-stream"` and formats chunks as `data: <json>\n\n`, terminating with `data: [DONE]\n\n`.

```python
import asyncio
import json
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient

app = FastAPI()


async def simulated_token_stream() -> AsyncGenerator[str, None]:
    tokens = ["Global", " markets", " closed", " higher", " today."]
    for token in tokens:
        await asyncio.sleep(0.01)  # Simulate model latency
        payload = json.dumps({"delta": token})
        yield f"data: {payload}\n\n"
    yield "data: [DONE]\n\n"


@app.get("/stream-chat")
def stream_chat():
    return StreamingResponse(
        simulated_token_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disables proxy buffering
        },
    )


client = TestClient(app)
with client.stream("GET", "/stream-chat") as resp:
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/event-stream")
    lines = [line if isinstance(line, str) else line.decode("utf-8") for line in resp.iter_lines() if line]
    assert len(lines) == 6
    assert '{"delta": "Global"}' in lines[0]
    assert "[DONE]" in lines[-1]
```

## Likely follow-ups

- Why is `X-Accel-Buffering: no` required when deploying behind Nginx or Azure Application Gateway?
- How should the client parse SSE frames using browser `EventSource` or `fetch`?

---

[← Q0806](../../batch_09_genai_services_fastapi/0806_testing_genai_endpoints_with_fastapi_testclient_and_mocking/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0808 →](../../batch_09_genai_services_fastapi/0808_streaming_langchain_chat_model_events_over_fastapi/README.md)
