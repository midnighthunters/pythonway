# Q0811 · Managing WebSocket connection pools and heartbeats

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI WebSockets | Medium |

## Question

Write Python code for a WebSocket connection manager that tracks active connections by user ID, broadcasts messages, and cleans up dead connections.

## Answer

```python
from typing import Dict, List
from fastapi import WebSocket


class WebSocketConnectionManager:
    def __init__(self):
        # Maps user_id -> list of active WebSockets (support multiple tabs)
        self.active_connections: Dict[str, List[WebSocket]] = {}

    def connect(self, user_id: str, websocket: WebSocket) -> None:
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str) -> None:
        sockets = self.active_connections.get(user_id, [])
        for ws in sockets:
            await ws.send_text(message)


manager = WebSocketConnectionManager()
mock_ws1 = object()
mock_ws2 = object()

manager.connect("user_alice", mock_ws1)
manager.connect("user_alice", mock_ws2)
assert len(manager.active_connections["user_alice"]) == 2

manager.disconnect("user_alice", mock_ws1)
assert len(manager.active_connections["user_alice"]) == 1
manager.disconnect("user_alice", mock_ws2)
assert "user_alice" not in manager.active_connections
```

## Likely follow-ups

- How does the server detect half-open TCP connections when a client laptop goes to sleep?
- What heartbeat interval is recommended to prevent cloud NAT gateways from dropping idle WebSocket sockets?

---

[← Q0810](../../batch_09_genai_services_fastapi/0810_bidirectional_websockets_for_interactive_agent_steering/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0812 →](../../batch_09_genai_services_fastapi/0812_asynchronous_job_submission_pattern_202_accepted_and_polling/README.md)
