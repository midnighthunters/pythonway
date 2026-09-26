"""
Verification Test Suite for Project 007: Conditional Edges, Dynamic Routing & Graph Cycles
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import build_refinement_graph, should_continue, CodeRefinementState


def test_router_logic():
    print("Testing 'should_continue' conditional routing logic...")

    # Case 1: High quality score -> should route to publisher
    state_approved: CodeRefinementState = {
        "task": "test",
        "current_code": "def foo(): pass",
        "quality_score": 9,
        "critique": "Looks great",
        "iteration": 1,
        "max_iterations": 3,
        "cycle_history": [],
    }
    decision = should_continue(state_approved)
    assert decision == "publisher", f"Expected 'publisher', got '{decision}'"
    print("  [PASSED] Score >= 8 routes directly to publisher.")

    # Case 2: Low quality score + iterations remaining -> should loop back to coder
    state_loop: CodeRefinementState = {
        "task": "test",
        "current_code": "def foo(): pass",
        "quality_score": 5,
        "critique": "Needs validation",
        "iteration": 1,
        "max_iterations": 3,
        "cycle_history": [],
    }
    decision = should_continue(state_loop)
    assert decision == "coder", f"Expected 'coder', got '{decision}'"
    print("  [PASSED] Score < 8 with iter < max routes to coder (cycle).")

    # Case 3: Low quality score + max iterations reached -> guardrail exit to publisher
    state_max_iter: CodeRefinementState = {
        "task": "test",
        "current_code": "def foo(): pass",
        "quality_score": 6,
        "critique": "Still minor issues",
        "iteration": 3,
        "max_iterations": 3,
        "cycle_history": [],
    }
    decision = should_continue(state_max_iter)
    assert decision == "publisher", f"Expected 'publisher', got '{decision}'"
    print("  [PASSED] Iteration >= max_iter triggers guardrail exit to publisher.")


def test_graph_compilation_and_execution():
    print("\nTesting graph compilation and live execution...")
    graph = build_refinement_graph()
    assert graph is not None, "Graph compilation returned None"
    print("  [PASSED] Graph compiled successfully.")

    # Run quick test task
    initial_state = {
        "task": "Write a Python function `add(a: int, b: int) -> int` that returns the sum.",
        "current_code": "",
        "quality_score": 0,
        "critique": "",
        "iteration": 0,
        "max_iterations": 2,
        "cycle_history": ["Session started"],
    }

    result = graph.invoke(initial_state)

    assert "current_code" in result, "Missing current_code in output state"
    assert len(result["current_code"]) > 0, "Generated code is empty"
    assert "quality_score" in result, "Missing quality_score in output state"
    assert result["iteration"] >= 1, "Graph did not run at least 1 iteration"
    assert len(result["cycle_history"]) >= 3, "Cycle history did not accumulate steps"
    print(f"  [PASSED] Graph executed cleanly! Iterations: {result['iteration']}, Final Score: {result['quality_score']}/10")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 007")
    print("=" * 60)
    test_router_logic()
    test_graph_compilation_and_execution()
    print("\n[ALL TESTS PASSED] Project 007 verified successfully!")
