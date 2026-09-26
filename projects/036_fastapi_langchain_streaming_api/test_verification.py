"""
Test verification suite for Project 036: FastAPI + LangChain Token Streaming API
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from fastapi.testclient import TestClient
from main import app, build_barista_chain, RUN_TELEMETRY_STORE


def test_chain_construction():
    chain = build_barista_chain()
    assert chain is not None


def test_sse_streaming_endpoint():
    RUN_TELEMETRY_STORE.clear()
    client = TestClient(app)

    tokens_received = []
    received_metadata = False
    received_telemetry = False
    received_done = False
    run_id = None

    with client.stream("POST", "/chat/stream", json={"query": "What is an Americano?", "user_id": "test_user"}) as res:
        assert res.status_code == 200
        assert "text/event-stream" in res.headers["content-type"]

        for line in res.iter_lines():
            if not line:
                continue
            if line.startswith("data: "):
                payload_str = line[6:]
                if payload_str == "[DONE]":
                    received_done = True
                    break
                payload = json.loads(payload_str)
                event_type = payload.get("type")
                if event_type == "metadata":
                    received_metadata = True
                    run_id = payload.get("run_id")
                elif event_type == "token":
                    tokens_received.append(payload.get("content", ""))
                elif event_type == "telemetry":
                    received_telemetry = True

    assert received_metadata, "Failed to receive metadata event"
    assert len(tokens_received) > 0, "No tokens were streamed"
    assert received_telemetry, "Failed to receive telemetry event"
    assert received_done, "Failed to receive [DONE] terminal event"
    assert run_id is not None
    assert run_id in RUN_TELEMETRY_STORE


def test_telemetry_endpoint():
    client = TestClient(app)
    res = client.get("/telemetry/runs")
    assert res.status_code == 200
    data = res.json()
    assert "total_runs" in data
    assert "runs" in data
    assert data["total_runs"] >= 1


if __name__ == "__main__":
    test_chain_construction()
    test_sse_streaming_endpoint()
    test_telemetry_endpoint()
    print("Project 036: All verification tests PASSED successfully!")
