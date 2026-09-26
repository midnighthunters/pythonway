"""
Test verification suite for Project 045: VectorDB + A2A Shared Blackboard Memory
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    SharedSemanticBlackboard,
    BaristaAgent,
    PastryChefAgent,
    InventoryAgent,
    CafeCuratorAgent,
)


def test_blackboard_post_and_query():
    bb = SharedSemanticBlackboard()
    e1 = bb.post("Agent1", "Espresso", "Notes of chocolate and hazelnut", tags=["coffee"])
    e2 = bb.post("Agent2", "Scone", "Warm buttery blueberry pastry", tags=["pastry"])

    assert len(bb.entries) == 2
    assert e1.entry_id == "bb_fact_001"
    assert e2.entry_id == "bb_fact_002"

    # Query for coffee
    results = bb.query("dark roast espresso chocolate", top_k=1)
    assert len(results) == 1
    assert results[0]["author_agent"] == "Agent1"
    assert results[0]["similarity_score"] > 0.0

    # Query with exclude_author
    filtered = bb.query("espresso", top_k=2, exclude_author="Agent1")
    for r in filtered:
        assert r["author_agent"] != "Agent1"


def test_multi_agent_blackboard_collaboration():
    bb = SharedSemanticBlackboard()
    barista = BaristaAgent(bb)
    baker = PastryChefAgent(bb)
    inventory = InventoryAgent(bb)
    curator = CafeCuratorAgent(bb)

    # Agents write facts
    barista.record_morning_calibration()
    baker.record_morning_bake()
    inventory.record_deliveries()

    assert len(bb.entries) == 3

    # Curator queries and synthesizes
    result = curator.design_featured_pairing()
    assert result["curator"] == "CafeCuratorAgent"
    assert len(result["blackboard_insights_used"]) >= 2
    synthesis = result["daily_special_synthesis"]
    assert isinstance(synthesis, str)
    assert len(synthesis) > 30


if __name__ == "__main__":
    test_blackboard_post_and_query()
    test_multi_agent_blackboard_collaboration()
    print("Project 045: All verification tests PASSED successfully!")
