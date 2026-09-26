"""
Verification Test Suite for Project 006: StateGraph Fundamentals & Reducers
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, START, END
from main import build_vacation_graph, VacationPlanState


def test_vacation_graph_execution():
    print("Testing Vacation Plan Graph live execution...")
    graph = build_vacation_graph()
    assert graph is not None, "Graph compilation returned None"

    initial_state: VacationPlanState = {
        "destination": "Paris, France",
        "current_status": "Initial",
        "packing_list": [],
        "estimated_cost": 0,
    }

    result = graph.invoke(initial_state)

    # 1. Test Overwrite: Status should be the final node's status, NOT "Initial"
    assert result["current_status"] == "Ready to travel!", f"Expected 'Ready to travel!', got '{result['current_status']}'"
    print("  [PASSED] Default overwrite behavior verified (status updated to final node).")

    # 2. Test List Reducer: Packing list should have items from all 3 nodes accumulated
    assert len(result["packing_list"]) >= 5, f"Expected at least 5 items, got {len(result['packing_list'])}"
    print(f"  [PASSED] List append reducer verified ({len(result['packing_list'])} items accumulated without data loss).")

    # 3. Test Number Reducer: 150 + 50 + 25 = 225
    assert result["estimated_cost"] == 225, f"Expected cost 225, got {result['estimated_cost']}"
    print(f"  [PASSED] Number sum reducer verified (Total cost = ${result['estimated_cost']}).")


def test_isolated_reducer_behavior():
    print("\nTesting isolated reducer logic...")

    class MiniState(TypedDict):
        text: str
        items: Annotated[List[str], operator.add]
        counter: Annotated[int, operator.add]

    b = StateGraph(MiniState)
    b.add_node("n1", lambda s: {"text": "A", "items": ["item1"], "counter": 10})
    b.add_node("n2", lambda s: {"text": "B", "items": ["item2"], "counter": 20})
    b.add_edge(START, "n1")
    b.add_edge("n1", "n2")
    b.add_edge("n2", END)

    app = b.compile()
    out = app.invoke({"text": "start", "items": [], "counter": 0})

    assert out["text"] == "B", "Overwrite failed"
    assert out["items"] == ["item1", "item2"], "List reducer failed"
    assert out["counter"] == 30, "Int sum reducer failed"
    print("  [PASSED] Isolated reducer mechanics verified 100%.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 006")
    print("=" * 60)
    test_vacation_graph_execution()
    test_isolated_reducer_behavior()
    print("\n[ALL TESTS PASSED] Project 006 verified successfully!")
