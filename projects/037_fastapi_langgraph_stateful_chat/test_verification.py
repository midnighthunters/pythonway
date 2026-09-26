"""
Test verification suite for Project 037: FastAPI + LangGraph Stateful Chatbot
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from main import app


def test_stateful_multi_turn_and_memory():
    client = TestClient(app)
    thread_id = "test_thread_alpha"

    # Turn 1
    t1_res = client.post(f"/chat/{thread_id}", json={"message": "Hi, my name is Alice and I love oat milk lattes."})
    assert t1_res.status_code == 200
    d1 = t1_res.json()
    assert d1["working_memory"]["customer_name"] == "Alice"
    assert "oat milk" in d1["working_memory"]["preferences"]
    assert d1["working_memory"]["turn_count"] == 1

    # Turn 2
    t2_res = client.post(f"/chat/{thread_id}", json={"message": "Can you recommend a snack?"})
    assert t2_res.status_code == 200
    d2 = t2_res.json()
    assert d2["working_memory"]["customer_name"] == "Alice"
    assert "oat milk" in d2["working_memory"]["preferences"]
    assert d2["working_memory"]["turn_count"] == 2
    assert d2["total_messages"] >= 4  # 2 user + 2 assistant messages


def test_thread_state_inspection():
    client = TestClient(app)
    thread_id = "test_thread_inspect"

    client.post(f"/chat/{thread_id}", json={"message": "Hello, my name is Bob."})
    state_res = client.get(f"/chat/{thread_id}/state")
    assert state_res.status_code == 200
    data = state_res.json()
    assert data["thread_id"] == thread_id
    assert data["working_memory"]["customer_name"] == "Bob"
    assert len(data["messages"]) == 2  # 1 human + 1 AI


def test_thread_isolation():
    client = TestClient(app)
    # Alice thread
    client.post("/chat/thread_alice", json={"message": "My name is Alice and I like decaf."})
    # Bob thread
    client.post("/chat/thread_bob", json={"message": "Hello, what's good today?"})

    res_bob = client.get("/chat/thread_bob/state")
    data_bob = res_bob.json()
    assert data_bob["working_memory"]["customer_name"] is None
    assert "decaf" not in data_bob["working_memory"]["preferences"]


def test_nonexistent_thread_404():
    client = TestClient(app)
    res = client.get("/chat/completely_unknown_thread/state")
    assert res.status_code == 404


if __name__ == "__main__":
    test_stateful_multi_turn_and_memory()
    test_thread_state_inspection()
    test_thread_isolation()
    test_nonexistent_thread_404()
    print("Project 037: All verification tests PASSED successfully!")
