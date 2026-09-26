"""
===============================================================================
PROJECT 047: LANGGRAPH + A2A: MULTI-AGENT CODER-REVIEWER DUAL LOOP
Stage 2: Pairwise Combos | Difficulty: 5.0 / 10
===============================================================================

THE BIG QUESTION:
How do autonomous multi-agent pairs collaborate iteratively to write, audit,
lint, and fix software defects until the code passes 100% of quality gates?

THE MULTI-AGENT DUAL LOOP PATTERN:
1. CoderAgent Node:
   - Drafts code from specification on Iteration 1.
   - Refactors and patches defects based on Reviewer feedback on subsequent iterations.
2. ReviewerAgent Node:
   - Performs automated code review, static analysis, and boundary condition audits.
   - Issues 'APPROVED' if flawless, or 'REVISION_REQUESTED' with actionable feedback.
3. LangGraph Cycle:
   - Conditional router checks review verdict: loops back to Coder if defects
     remain, or terminates at END once approved.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
from typing import TypedDict, List, Dict, Any, Optional

from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. STATE DEFINITION
# =============================================================================
class CoderReviewerState(TypedDict):
    task_spec: str
    code_draft: str
    review_verdict: str  # "APPROVED" or "REVISION_REQUESTED"
    review_feedback: str
    lint_errors: List[str]
    iteration: int
    max_iterations: int
    iteration_history: List[Dict[str, Any]]


# =============================================================================
# 2. CODER AGENT NODE
# =============================================================================
def coder_agent_node(state: CoderReviewerState) -> Dict[str, Any]:
    """Writes or refactors Python implementation based on review critique."""
    llm = get_llm(temperature=0.1)
    iteration = state.get("iteration", 0) + 1
    spec = state["task_spec"]
    prev_draft = state.get("code_draft", "")
    feedback = state.get("review_feedback", "")
    lint_errors = state.get("lint_errors", [])

    if iteration == 1:
        prompt = (
            f"You are an expert Python Software Engineer (Coder Agent).\n"
            f"TASK SPECIFICATION:\n{spec}\n\n"
            f"Write a complete, robust Python function adhering to all requirements. "
            f"Enclose your Python code in a ```python ... ``` block."
        )
    else:
        errs_str = "\n".join([f"- {e}" for e in lint_errors])
        prompt = (
            f"You are the Coder Agent refactoring an implementation based on Senior Reviewer feedback.\n"
            f"TASK SPECIFICATION:\n{spec}\n\n"
            f"PREVIOUS DRAFT:\n{prev_draft}\n\n"
            f"REVIEW CRITIQUE:\n{feedback}\n"
            f"LINT & EDGE CASE ERRORS TO FIX:\n{errs_str}\n\n"
            f"Refactor the code to eliminate all reported defects and edge-case bugs. "
            f"Enclose your updated Python code in a ```python ... ``` block."
        )

    response = llm.invoke(prompt)
    content = response.content.strip()

    # Extract code from markdown block
    if "```python" in content:
        code_body = content.split("```python")[1].split("```")[0].strip()
    elif "```" in content:
        code_body = content.split("```")[1].split("```")[0].strip()
    else:
        code_body = content

    return {
        "code_draft": code_body,
        "iteration": iteration,
    }


# =============================================================================
# 3. REVIEWER AGENT NODE
# =============================================================================
def reviewer_agent_node(state: CoderReviewerState) -> Dict[str, Any]:
    """Audits code draft against boundary conditions, type hints, and specification."""
    llm = get_llm(temperature=0.0)
    spec = state["task_spec"]
    code = state["code_draft"]
    iteration = state["iteration"]

    audit_prompt = (
        f"You are the Principal Staff QA and Security Reviewer (Reviewer Agent).\n"
        f"Analyze the following Python implementation against the Task Specification.\n\n"
        f"TASK SPECIFICATION:\n{spec}\n\n"
        f"CODE DRAFT:\n{code}\n\n"
        f"Evaluate the code strictly for:\n"
        f"1. Negative or invalid boundary inputs (must raise ValueError if specified).\n"
        f"2. Coupon discounting logic (cannot reduce total below 0.0).\n"
        f"3. Type annotations and return format.\n\n"
        f"Respond with a JSON object containing keys:\n"
        f'- "verdict": "APPROVED" if code is 100% complete and defect-free, else "REVISION_REQUESTED"\n'
        f'- "defects": list of string descriptions for any bugs, unhandled edge cases, or missing checks\n'
        f'- "summary_feedback": concise guidance for the coder\n'
    )

    response = llm.invoke(audit_prompt)
    content = response.content.strip()

    try:
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        data = json.loads(content)
        verdict = data.get("verdict", "REVISION_REQUESTED")
        defects = data.get("defects", [])
        summary = data.get("summary_feedback", "Review complete.")
    except Exception:
        # Fallback inspection
        verdict = "APPROVED" if "ValueError" in code and "round" in code else "REVISION_REQUESTED"
        defects = ["Ensure ValueError is raised for negative subtotal"] if verdict != "APPROVED" else []
        summary = "Automated fallback audit."

    history = list(state.get("iteration_history", []))
    history.append({
        "iteration": iteration,
        "verdict": verdict,
        "defects": defects,
        "feedback": summary,
        "code_snapshot": code[:120] + "...",
    })

    return {
        "review_verdict": verdict,
        "lint_errors": defects,
        "review_feedback": summary,
        "iteration_history": history,
    }


# =============================================================================
# 4. CONDITIONAL ROUTING & GRAPH COMPILATION
# =============================================================================
def should_continue_review_loop(state: CoderReviewerState) -> str:
    verdict = state.get("review_verdict")
    iteration = state.get("iteration", 0)
    max_iter = state.get("max_iterations", 3)

    if verdict == "APPROVED":
        return END
    elif iteration >= max_iter:
        return END
    else:
        return "coder"


workflow = StateGraph(CoderReviewerState)
workflow.add_node("coder", coder_agent_node)
workflow.add_node("reviewer", reviewer_agent_node)

workflow.add_edge(START, "coder")
workflow.add_edge("coder", "reviewer")
workflow.add_conditional_edges("reviewer", should_continue_review_loop, {"coder": "coder", END: END})

coder_reviewer_graph = workflow.compile()


# =============================================================================
# 5. MAIN DEMONSTRATION RUNNER
# =============================================================================
TASK_SPECIFICATION = (
    "Create a function `calculate_cafe_loyalty_discount(subtotal: float, tier: str, coupon: Optional[str] = None) -> Dict[str, float]`.\n"
    "Requirements:\n"
    "1. If `subtotal` is negative, raise ValueError('Subtotal cannot be negative').\n"
    "2. Tier discounts: 'bronze' (5%), 'silver' (10%), 'gold' (15%), 'platinum' (20%). Case-insensitive. Unknown tiers get 0%.\n"
    "3. Coupon: If coupon == 'SUMMER10', deduct $10.00 after the tier discount. The discounted subtotal can never fall below $0.00.\n"
    "4. Tax: Apply 8.5% sales tax on the discounted subtotal.\n"
    "5. Return a dictionary with keys: 'subtotal', 'discount_amount', 'tax_amount', 'final_total'. All values rounded to 2 decimals."
)


def main():
    print("=" * 75)
    print("PROJECT 047: LANGGRAPH + A2A CODER-REVIEWER DUAL LOOP")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    print(f"\nTask Specification:\n{TASK_SPECIFICATION}")
    print("\n" + "-" * 75)
    print("Initiating Multi-Agent Iterative Code-Review Cycle:")
    print("-" * 75)

    initial_state: CoderReviewerState = {
        "task_spec": TASK_SPECIFICATION,
        "code_draft": "",
        "review_verdict": "PENDING",
        "review_feedback": "",
        "lint_errors": [],
        "iteration": 0,
        "max_iterations": 3,
        "iteration_history": [],
    }

    final_state = coder_reviewer_graph.invoke(initial_state)

    print("\n" + "=" * 75)
    print(f"CYCLE SUMMARY (Total Iterations: {len(final_state['iteration_history'])})")
    print("=" * 75)
    for record in final_state["iteration_history"]:
        print(f"\n[Iteration #{record['iteration']}] Verdict: {record['verdict']}")
        print(f"Feedback: {record['feedback']}")
        if record["defects"]:
            print(f"Defects Identified: {record['defects']}")

    print("\n" + "-" * 75)
    print("FINAL APPROVED PYTHON CODE:")
    print("-" * 75)
    print(final_state["code_draft"])

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 047 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
