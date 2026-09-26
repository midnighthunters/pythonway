"""
Test verification suite for Project 047: LangGraph + A2A Coder-Reviewer Dual Loop
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import (
    coder_reviewer_graph,
    coder_agent_node,
    reviewer_agent_node,
    should_continue_review_loop,
    TASK_SPECIFICATION,
    CoderReviewerState,
)


def test_routing_logic():
    # Approved state should end
    approved_state: CoderReviewerState = {
        "task_spec": "dummy",
        "code_draft": "dummy",
        "review_verdict": "APPROVED",
        "review_feedback": "",
        "lint_errors": [],
        "iteration": 1,
        "max_iterations": 3,
        "iteration_history": [],
    }
    assert should_continue_review_loop(approved_state) == "__end__"

    # Defect state before max iterations should loop to coder
    defect_state: CoderReviewerState = {
        "task_spec": "dummy",
        "code_draft": "dummy",
        "review_verdict": "REVISION_REQUESTED",
        "review_feedback": "Fix bugs",
        "lint_errors": ["Error 1"],
        "iteration": 1,
        "max_iterations": 3,
        "iteration_history": [],
    }
    assert should_continue_review_loop(defect_state) == "coder"

    # Defect state reaching max iterations should terminate
    max_state: CoderReviewerState = {
        "task_spec": "dummy",
        "code_draft": "dummy",
        "review_verdict": "REVISION_REQUESTED",
        "review_feedback": "Fix bugs",
        "lint_errors": ["Error 1"],
        "iteration": 3,
        "max_iterations": 3,
        "iteration_history": [],
    }
    assert should_continue_review_loop(max_state) == "__end__"


def test_end_to_end_coder_reviewer_loop():
    initial_state: CoderReviewerState = {
        "task_spec": TASK_SPECIFICATION,
        "code_draft": "",
        "review_verdict": "PENDING",
        "review_feedback": "",
        "lint_errors": [],
        "iteration": 0,
        "max_iterations": 2,
        "iteration_history": [],
    }
    result = coder_reviewer_graph.invoke(initial_state)

    assert result["iteration"] >= 1
    assert len(result["iteration_history"]) >= 1
    assert "def calculate_cafe_loyalty_discount" in result["code_draft"]

    # Verify python syntax by compiling the code draft
    code = result["code_draft"]
    compiled = compile(code, "<string>", "exec")
    assert compiled is not None


if __name__ == "__main__":
    test_routing_logic()
    test_end_to_end_coder_reviewer_loop()
    print("Project 047: All verification tests PASSED successfully!")
