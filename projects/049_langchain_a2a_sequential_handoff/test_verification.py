"""
Test verification suite for Project 049: LangChain + A2A Sequential Role Handoff
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    HandoffEnvelope,
    researcher_agent,
    analyst_agent,
    writer_agent,
    build_sequential_handoff_pipeline,
)


def test_handoff_envelope_transitions():
    env1 = HandoffEnvelope(
        sender_role="AgentA",
        recipient_role="AgentB",
        step_name="step_one",
        summary="Initial draft",
        payload={"count": 1},
    )
    assert len(env1.lineage) == 0

    env2 = env1.record_transition(
        next_recipient="AgentC",
        next_step="step_two",
        new_summary="Second draft",
        updated_payload={"count": 2},
    )
    assert len(env2.lineage) == 1
    assert env2.lineage[0]["sender"] == "AgentA"
    assert env2.lineage[0]["recipient"] == "AgentB"
    assert env2.sender_role == "AgentB"
    assert env2.recipient_role == "AgentC"
    assert env2.payload["count"] == 2


def test_sequential_handoff_pipeline():
    pipeline = build_sequential_handoff_pipeline()
    topic = "Colombian Geisha anaerobic fermentation"

    final_env = pipeline.invoke(topic)

    assert isinstance(final_env, HandoffEnvelope)
    assert len(final_env.lineage) == 2  # Researcher->Analyst, Analyst->Writer
    assert "agronomy_research" in final_env.payload
    assert "sensory_analysis" in final_env.payload
    assert "menu_feature_card" in final_env.payload
    assert final_env.recipient_role == "CustomerDeliverySystem"

    card = final_env.payload["menu_feature_card"]
    assert isinstance(card, str)
    assert len(card) > 20


if __name__ == "__main__":
    test_handoff_envelope_transitions()
    test_sequential_handoff_pipeline()
    print("Project 049: All verification tests PASSED successfully!")
