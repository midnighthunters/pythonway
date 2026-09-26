"""
===============================================================================
PROJECT 033: REAL-TIME STREAMING: SERVER-SENT EVENTS (SSE) & WEBSOCKETS
Stage 1: Pure Fundamentals | Difficulty: 3.0 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
How do AI applications stream model tokens to users with near-zero latency?

STREAMING PROTOCOLS:
1. Server-Sent Events (SSE): HTTP-based one-way stream (`text/event-stream`).
   Ideal for standard AI chatbots streaming tokens to browsers.
2. WebSockets (WS): Persistent, full-duplex bidirectional TCP sockets.
   Ideal for multi-user AI collaboration, live voice/audio, and bidirectional control.
3. Connection Management: Managing active sockets, heartbeats, and graceful disconnection.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
import asyncio
from typing import List, AsyncGenerator
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. WEBSOCKET CONNECTION MANAGER
# =============================================================================
class ConnectionManager:
    """Manages active full-duplex WebSocket connections and broadcasting."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_event(self, event_data: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(json.dumps(event_data))
            except Exception:
                self.disconnect(connection)


manager = ConnectionManager()
app = FastAPI(title="Real-Time Streaming Service (SSE & WebSockets)", version="1.0.0")


# =============================================================================
# 2. SERVER-SENT EVENTS (SSE) STREAMING
# =============================================================================
async def sse_token_generator(prompt: str) -> AsyncGenerator[str, None]:
    """
    Streams tokens using the standard SSE wire protocol format:
      data: <payload>\n\n
    """
    llm = get_llm(temperature=0.2)
    # Stream real chunks from Groq LLM
    stream = llm.stream(prompt)

    chunk_idx = 0
    for chunk in stream:
        token_str = chunk.content
        if token_str:
            event_payload = json.dumps({"index": chunk_idx, "token": token_str})
            yield f"data: {event_payload}\n\n"
            chunk_idx += 1
            await asyncio.sleep(0.01)

    # Terminal stream event
    yield f"data: {json.dumps({'event': 'DONE', 'total_tokens': chunk_idx})}\n\n"


@app.get("/stream/sse")
async def stream_sse(prompt: str = Query(default="Explain cold brew extraction in 2 sentences")):
    """Streams LLM tokens via Server-Sent Events (SSE)."""
    return StreamingResponse(
        sse_token_generator(prompt),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


# =============================================================================
# 3. WEBSOCKET FULL-DUPLEX CHAT ENDPOINT
# =============================================================================
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """
    Full-duplex WebSocket connection:
    Client sends JSON query -> Server streams back token frames -> Sends completion signal.
    """
    await manager.connect(websocket)
    try:
        while True:
            raw_text = await websocket.receive_text()
            data = json.loads(raw_text)
            user_prompt = data.get("prompt", "Hello")

            llm = get_llm(temperature=0.1)
            stream = llm.stream(user_prompt)

            idx = 0
            for chunk in stream:
                token = chunk.content
                if token:
                    frame = {"type": "TOKEN", "index": idx, "token": token}
                    await websocket.send_text(json.dumps(frame))
                    idx += 1

            # End of stream frame
            await websocket.send_text(json.dumps({"type": "COMPLETED", "tokens_sent": idx}))

    except WebSocketDisconnect:
        manager.disconnect(websocket)


# =============================================================================
# 4. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 033: REAL-TIME STREAMING: SERVER-SENT EVENTS (SSE) & WEBSOCKETS")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    client = TestClient(app)

    # -------------------------------------------------------------------------
    # PART 1: TEST SERVER-SENT EVENTS (SSE)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("1. TESTING SSE STREAMING (GET /stream/sse)")
    print("-" * 75)
    sse_prompt = "What is the optimal water temperature for brewing espresso? (Answer in 1 sentence)"
    print(f"Prompt: \"{sse_prompt}\"\n\nLive SSE Stream Output:")

    full_sse_text = ""
    with client.stream("GET", "/stream/sse", params={"prompt": sse_prompt}) as response:
        for line in response.iter_lines():
            if line.startswith("data: "):
                payload_str = line.replace("data: ", "").strip()
                payload = json.loads(payload_str)
                if "token" in payload:
                    print(payload["token"], end="", flush=True)
                    full_sse_text += payload["token"]
                elif payload.get("event") == "DONE":
                    print(f"\n[SSE STREAM COMPLETED: {payload['total_tokens']} tokens]")

    # -------------------------------------------------------------------------
    # PART 2: TEST WEBSOCKET FULL-DUPLEX STREAMING
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("2. TESTING WEBSOCKET BIDIRECTIONAL STREAMING (/ws/chat)")
    print("-" * 75)
    ws_prompt = "Name 3 famous coffee bean growing regions. (Answer as a bulleted list)"
    print(f"WebSocket Client Prompt: \"{ws_prompt}\"\n\nStreaming WebSocket Frames:")

    with client.websocket_connect("/ws/chat") as ws:
        # Send query
        ws.send_text(json.dumps({"prompt": ws_prompt}))

        while True:
            msg = ws.receive_text()
            frame = json.loads(msg)
            if frame.get("type") == "TOKEN":
                print(frame["token"], end="", flush=True)
            elif frame.get("type") == "COMPLETED":
                print(f"\n[WS STREAM COMPLETED: {frame['tokens_sent']} frames]")
                break

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 033 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
