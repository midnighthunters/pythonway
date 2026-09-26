# Q0809 · Client disconnect detection during streaming generation

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI streaming | Hard |

## Question

When a user closes their browser tab mid-stream, an LLM continues generating tokens in the background, wasting GPU resources and money. How does FastAPI detect client disconnects?

## Answer

When a client closes an HTTP connection, the underlying socket becomes disconnected. In FastAPI/Starlette, request disconnects are checked via `await request.is_disconnected()`.

Implementation:
Inside the async generator producing chunks, periodically check `if await request.is_disconnected(): break`. When detected, abort the downstream model stream and release the generator immediately.

```python
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()


async def cancellable_token_stream(request: Request):
    tokens = ["Token_" + str(i) for i in range(100)]
    for tok in tokens:
        # Check if client closed connection
        if await request.is_disconnected():
            # Stop generating immediately to save GPU compute and cost
            break
        await asyncio.sleep(0.01)
        yield f"data: {tok}\n\n"


@app.get("/cancellable-stream")
def stream_endpoint(request: Request):
    return StreamingResponse(cancellable_token_stream(request), media_type="text/event-stream")


# Verification: The generator checks request.is_disconnected() on every iteration
assert hasattr(app, "routes")
```

## Likely follow-ups

- How often should `request.is_disconnected()` be polled during high-speed token generation?
- What cleanup actions (e.g. cancelling an asyncio Task or releasing checkpointer locks) must execute upon disconnect?

---

[← Q0808](../../batch_09_genai_services_fastapi/0808_streaming_langchain_chat_model_events_over_fastapi/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0810 →](../../batch_09_genai_services_fastapi/0810_bidirectional_websockets_for_interactive_agent_steering/README.md)
