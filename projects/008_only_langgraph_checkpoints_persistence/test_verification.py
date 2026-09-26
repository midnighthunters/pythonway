"""
Verification Test Suite for Project 008: Checkpoints, MemorySaver & State Persistence
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from main import build_persistent_graph


def test_thread_persistence_and_isolation():
    print("Testing multi-turn thread persistence and cross-thread isolation...")

    memory = MemorySaver()
    graph = build_persistent_graph(checkpointer=memory)

    thread_a = {"configurable": {"thread_id": "test_thread_alpha"}}
    thread_b = {"configurable": {"thread_id": "test_thread_beta"}}

    # Turn 1 in Thread A
    res_a1 = graph.invoke(
        {"messages": [HumanMessage(content="My favorite color is Cerulean Blue.")], "session_notes": ["Init A"]},
        config=thread_a,
    )
    assert len(res_a1["messages"]) == 2, "Turn 1 should contain 2 messages (User + AI)"
    print("  [PASSED] Thread A Turn 1 completed.")

    # Turn 2 in Thread A (Asking to recall without passing previous message)
    res_a2 = graph.invoke(
        {"messages": [HumanMessage(content="What is my favorite color? Answer in one word.")], "session_notes": []},
        config=thread_a,
    )
    assert len(res_a2["messages"]) == 4, f"Turn 2 should accumulate 4 messages, got {len(res_a2['messages'])}"
    ai_answer = res_a2["messages"][-1].content.lower()
    assert "blue" in ai_answer or "cerulean" in ai_answer, f"Assistant failed to recall state: {ai_answer}"
    print(f"  [PASSED] Thread A retained state across turns (Answer: '{ai_answer.strip()}').")

    # Turn 1 in Thread B (Isolation check)
    res_b1 = graph.invoke(
        {"messages": [HumanMessage(content="What is my favorite color? Answer in one word.")], "session_notes": ["Init B"]},
        config=thread_b,
    )
    assert len(res_b1["messages"]) == 2, f"Thread B should only have 2 messages, got {len(res_b1['messages'])}"
    b_answer = res_b1["messages"][-1].content.lower()
    assert "cerulean" not in b_answer, f"State leaked from Thread A to Thread B! Output: {b_answer}"
    print("  [PASSED] Thread B is strictly isolated from Thread A.")


def test_state_inspection_and_history():
    print("\nTesting checkpoint state inspection APIs...")

    memory = MemorySaver()
    graph = build_persistent_graph(checkpointer=memory)
    thread_cfg = {"configurable": {"thread_id": "history_test_thread"}}

    graph.invoke({"messages": [HumanMessage(content="Hello")], "session_notes": ["Step 1"]}, config=thread_cfg)
    graph.invoke({"messages": [HumanMessage(content="Second message")], "session_notes": ["Step 2"]}, config=thread_cfg)

    # Test get_state
    state = graph.get_state(thread_cfg)
    assert state is not None, "get_state() returned None"
    assert "messages" in state.values, "Missing 'messages' in state values"
    assert len(state.values["messages"]) == 4, f"Expected 4 messages, got {len(state.values['messages'])}"
    assert len(state.values["session_notes"]) >= 2, "Session notes were not accumulated"
    print("  [PASSED] graph.get_state() accurately inspects live state values.")

    # Test get_state_history
    history = list(graph.get_state_history(thread_cfg))
    assert len(history) >= 2, f"Expected at least 2 snapshots in history, got {len(history)}"
    print(f"  [PASSED] graph.get_state_history() returned {len(history)} historical snapshots.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 008")
    print("=" * 60)
    test_thread_persistence_and_isolation()
    test_state_inspection_and_history()
    print("\n[ALL TESTS PASSED] Project 008 verified successfully!")
