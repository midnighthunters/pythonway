"""
Verification Test Suite for Project 033: Real-Time Streaming (SSE & WebSockets)
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from fastapi.testclient import TestClient
from main import app, manager


def test_sse_endpoint_stream():
    print("Testing SSE streaming endpoint...")
    client = TestClient(app)

    tokens_received = 0
    done_received = False

    with client.stream("GET", "/stream/sse", params={"prompt": "Say hello in one word"}) as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

        for line in response.iter_lines():
            if line.startswith("data: "):
                raw = line.replace("data: ", "").strip()
                payload = json.loads(raw)
                if "token" in payload:
                    tokens_received += 1
                elif payload.get("event") == "DONE":
                    done_received = True

    assert tokens_received > 0, "No tokens received from SSE stream"
    assert done_received, "Terminal SSE completion event missing"
    print(f"  [PASSED] SSE endpoint streamed {tokens_received} tokens cleanly.")


def test_websocket_streaming():
    print("\nTesting WebSocket bidirectional streaming...")
    client = TestClient(app)

    with client.websocket_connect("/ws/chat") as ws:
        ws.send_text(json.dumps({"prompt": "Say 'OK'"}))

        tokens = []
        completed = False
        while True:
            msg = ws.receive_text()
            data = json.loads(msg)
            if data.get("type") == "TOKEN":
                tokens.append(data["token"])
            elif data.get("type") == "COMPLETED":
                completed = True
                break

        assert len(tokens) > 0, "No tokens streamed over WebSocket"
        assert completed, "COMPLETED frame missing from WebSocket stream"

    print("  [PASSED] WebSocket full-duplex token streaming verified.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 033")
    print("=" * 60)
    test_sse_endpoint_stream()
    test_websocket_streaming()
    print("\n[ALL TESTS PASSED] Project 033 verified successfully!")
