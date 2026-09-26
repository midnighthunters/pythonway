"""
Verification Test Suite for Project 009: Human-in-the-Loop, Interrupts & State Modification
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from langgraph.checkpoint.memory import MemorySaver
from main import build_hitl_wire_transfer_graph


def test_hitl_approval_and_state_modification():
    print("Testing HITL interrupt pause, state mutation, and approval resumption...")

    memory = MemorySaver()
    graph = build_hitl_wire_transfer_graph(checkpointer=memory)
    thread_cfg = {"configurable": {"thread_id": "test_hitl_approve"}}

    # Step 1: Initial invocation should run proposal and stop before execution_gate
    graph.invoke(
        {
            "request": "Transfer 10000 USD to Cloud Hosting LLC",
            "recipient": "",
            "amount": 0.0,
            "currency": "",
            "risk_level": "PENDING",
            "human_approved": False,
            "human_feedback": "",
            "execution_status": "DRAFT",
            "audit_trail": ["Start test"],
        },
        config=thread_cfg,
    )

    snapshot = graph.get_state(thread_cfg)
    assert snapshot.next == ("execution_gate",), f"Expected next to be ('execution_gate',), got {snapshot.next}"
    assert snapshot.values["amount"] == 10000.0, f"Expected amount 10000, got {snapshot.values['amount']}"
    print("  [PASSED] Execution correctly halted before 'execution_gate'.")

    # Step 2: Human modifies state (adjusts amount and marks approved)
    graph.update_state(
        thread_cfg,
        values={
            "amount": 9500.0,
            "human_approved": True,
            "human_feedback": "Approved with $500 discount",
        },
    )
    updated_snapshot = graph.get_state(thread_cfg)
    assert updated_snapshot.values["amount"] == 9500.0, "State modification failed"
    assert updated_snapshot.values["human_approved"] is True, "Approval flag failed to update"
    print("  [PASSED] graph.update_state() successfully mutated state prior to gate execution.")

    # Step 3: Resume execution
    final_output = graph.invoke(None, config=thread_cfg)
    assert final_output["execution_status"] == "COMPLETED", f"Expected COMPLETED, got {final_output['execution_status']}"
    assert final_output["amount"] == 9500.0, f"Expected 9500.0, got {final_output['amount']}"

    post_run_state = graph.get_state(thread_cfg)
    assert post_run_state.next == (), f"Expected graph to be finished, next is {post_run_state.next}"
    print("  [PASSED] Resumed graph successfully reached COMPLETED status.")


def test_hitl_rejection():
    print("\nTesting HITL rejection flow...")

    memory = MemorySaver()
    graph = build_hitl_wire_transfer_graph(checkpointer=memory)
    thread_cfg = {"configurable": {"thread_id": "test_hitl_reject"}}

    graph.invoke(
        {
            "request": "Transfer 50000 EUR to Unknown Entity",
            "recipient": "",
            "amount": 0.0,
            "currency": "",
            "risk_level": "PENDING",
            "human_approved": False,
            "human_feedback": "",
            "execution_status": "DRAFT",
            "audit_trail": ["Start test 2"],
        },
        config=thread_cfg,
    )

    snapshot = graph.get_state(thread_cfg)
    assert snapshot.next == ("execution_gate",), "Graph did not interrupt before execution gate"

    # Human supervisor denies transaction
    graph.update_state(
        thread_cfg,
        values={
            "human_approved": False,
            "human_feedback": "Rejected: Entity cannot be verified.",
        },
    )

    final_output = graph.invoke(None, config=thread_cfg)
    assert final_output["execution_status"] == "REJECTED", f"Expected REJECTED, got {final_output['execution_status']}"
    print("  [PASSED] Resumed graph successfully executed rejection branch.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 009")
    print("=" * 60)
    test_hitl_approval_and_state_modification()
    test_hitl_rejection()
    print("\n[ALL TESTS PASSED] Project 009 verified successfully!")
