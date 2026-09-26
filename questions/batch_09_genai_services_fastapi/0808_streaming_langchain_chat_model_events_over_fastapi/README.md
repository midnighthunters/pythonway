# Q0808 · Streaming LangChain chat model events over FastAPI

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI streaming | Medium |

## Question

Write Python code for a FastAPI streaming route that consumes an asynchronous token generator (simulating `model.astream()`) and formats events for the client.

## Answer

```python
import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient

app = FastAPI()


async def mock_model_astream(prompt: str):
    chunks = ["Analyzing", " trade", " break", " BRK-100"]
    for c in chunks:
        await asyncio.sleep(0.01)
        yield c


async def sse_event_generator(prompt: str):
    async for chunk in mock_model_astream(prompt):
        yield f"data: {json.dumps({'content': chunk})}\n\n"
    yield "data: [DONE]\n\n"


@app.post("/agent/stream")
def agent_stream(payload: dict):
    prompt = payload.get("prompt", "")
    return StreamingResponse(sse_event_generator(prompt), media_type="text/event-stream")


client = TestClient(app)
with client.stream("POST", "/agent/stream", json={"prompt": "Check trade"}) as response:
    raw_lines = [line if isinstance(line, str) else line.decode("utf-8") for line in response.iter_lines() if line]
    assert len(raw_lines) == 5
    assert '{"content": "Analyzing"}' in raw_lines[0]
```

## Likely follow-ups

- How does LangGraph's `astream_events(version="v2")` distinguish between LLM token deltas and intermediate tool execution events?
- How can custom metadata (e.g. citation links) be streamed as separate SSE event types?

---

[← Q0807](../../batch_09_genai_services_fastapi/0807_server_sent_events_streaming_with_streamingresponse/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0809 →](../../batch_09_genai_services_fastapi/0809_client_disconnect_detection_during_streaming_generation/README.md)
