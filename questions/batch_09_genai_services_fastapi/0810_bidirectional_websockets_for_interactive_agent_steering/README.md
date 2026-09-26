# Q0810 · Bidirectional WebSockets for interactive agent steering

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI WebSockets | Medium |

## Question

Write Python code for a FastAPI WebSocket endpoint allowing a user to stream chat messages, interrupt an agent mid-thought, and receive real-time status updates.

## Answer

While SSE is unidirectional (server-to-client), WebSockets provide full-duplex communication over a single TCP connection. This allows users to send steering commands or stop signals while the agent is actively streaming reasoning steps.

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.testclient import TestClient

app = FastAPI()


@app.websocket("/ws/agent")
async def agent_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == "STOP":
                await websocket.send_text("SYSTEM: Agent execution halted by user.")
            else:
                # Simulate agent response stream
                await websocket.send_text(f"AGENT_STEP: Processing query '{data}'")
                await websocket.send_text("AGENT_FINAL: Task finished.")
    except WebSocketDisconnect:
        pass


client = TestClient(app)
with client.websocket_connect("/ws/agent") as ws:
    ws.send_text("Analyze bond spread")
    msg1 = ws.receive_text()
    assert "AGENT_STEP: Processing" in msg1
    msg2 = ws.receive_text()
    assert "AGENT_FINAL: Task finished." in msg2

    ws.send_text("STOP")
    stop_msg = ws.receive_text()
    assert "halted by user" in stop_msg
```

## Likely follow-ups

- How does WebSocket authentication differ from standard HTTP header authentication?
- How do you handle load balancing WebSockets across multiple container instances using Redis pub/sub?

---

[← Q0809](../../batch_09_genai_services_fastapi/0809_client_disconnect_detection_during_streaming_generation/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0811 →](../../batch_09_genai_services_fastapi/0811_managing_websocket_connection_pools_and_heartbeats/README.md)
