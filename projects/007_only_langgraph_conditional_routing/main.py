"""
===============================================================================
PROJECT 007: CONDITIONAL EDGES, DYNAMIC ROUTING & GRAPH CYCLES
Stage 1: Pure Fundamentals | Difficulty: 2.5 / 10 (Intermediate)
===============================================================================

Core Concepts Demonstrated:
1. Conditional Routing: add_conditional_edges() evaluating runtime state.
2. Cyclic Execution (Loops): Looping back to worker nodes until quality standards are met.
3. Termination Guardrails: Enforcing max_iterations to prevent infinite loops.
4. Router Functions: Pure Python functions mapping state values to destination nodes.
===============================================================================
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
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. STATE DEFINITION
# =============================================================================
class CodeRefinementState(TypedDict):
    task: str
    current_code: str
    quality_score: int  # 1 to 10
    critique: str
    iteration: int
    max_iterations: int
    cycle_history: Annotated[List[str], operator.add]


# =============================================================================
# 2. NODES (WORKERS & EVALUATORS)
# =============================================================================
def coder_node(state: CodeRefinementState) -> dict:
    """Generates initial code or refines previous code using critique."""
    iter_num = state.get("iteration", 0) + 1
    print(f"\n--- [CODER NODE (Iteration {iter_num})] Writing/Refining code... ---")

    llm = get_llm(temperature=0.2)

    if iter_num == 1:
        prompt = (
            f"Write a Python function to solve this task:\n'{state['task']}'\n\n"
            "Include type hints and a docstring. Output ONLY the raw Python code block."
        )
    else:
        prompt = (
            f"Task: {state['task']}\n\n"
            f"Your Previous Code:\n{state['current_code']}\n\n"
            f"Critique / Flaws Found:\n{state['critique']}\n\n"
            "Rewrite the Python code addressing every critique point. Output ONLY the raw code."
        )

    response = llm.invoke(prompt)
    code = response.content.replace("```python", "").replace("```", "").strip()

    return {
        "current_code": code,
        "iteration": iter_num,
        "cycle_history": [f"Iteration {iter_num}: Code drafted/refined"],
    }


def evaluator_node(state: CodeRefinementState) -> dict:
    """Reviews code, spots missing edge cases, and awards a quality score (1 to 10)."""
    print(f"\n--- [EVALUATOR NODE] Reviewing code quality... ---")
    llm = get_llm(temperature=0.0)

    prompt = (
        f"You are a strict Principal Engineer reviewing this code:\n\n{state['current_code']}\n\n"
        f"Task Requirements: {state['task']}\n\n"
        "Evaluate correctness, edge cases (empty inputs, negative numbers, types), and clean style.\n"
        "Format your response EXACTLY as:\n"
        "SCORE: <integer 1 to 10>\n"
        "CRITIQUE: <concise actionable feedback>"
    )

    response = llm.invoke(prompt)
    lines = response.content.strip().split("\n")

    score = 7  # default fallback
    critique = "Add edge case validation."

    for line in lines:
        if line.startswith("SCORE:"):
            try:
                score = int(line.replace("SCORE:", "").strip())
            except ValueError:
                score = 7
        elif line.startswith("CRITIQUE:"):
            critique = line.replace("CRITIQUE:", "").strip()

    print(f" -> Evaluator Score : {score} / 10")
    print(f" -> Critique Notes  : {critique}")

    return {
        "quality_score": score,
        "critique": critique,
        "cycle_history": [f"Evaluation: Score {score}/10"],
    }


def publisher_node(state: CodeRefinementState) -> dict:
    """Final packaging node once quality threshold is achieved."""
    print("\n--- [PUBLISHER NODE] Packaging approved code for deployment... ---")
    return {
        "cycle_history": [f"Published code with final score {state['quality_score']}/10"],
    }


# =============================================================================
# 3. ROUTER FUNCTION (CONDITIONAL EDGE LOGIC)
# =============================================================================
def should_continue(state: CodeRefinementState) -> str:
    """
    Router Function:
    Inspects state and returns the name of the destination node.
    - If score >= 8 OR max_iterations reached -> 'publisher'
    - Otherwise -> 'coder' (LOOPS BACK!)
    """
    score = state.get("quality_score", 0)
    current_iter = state.get("iteration", 0)
    max_iter = state.get("max_iterations", 3)

    print(f"\n[ROUTER DECISION]: Score={score}, Iteration={current_iter}/{max_iter}")

    if score >= 8:
        print(" -> Decision: Quality threshold achieved (>= 8)! Routing to 'publisher' -> END.")
        return "publisher"

    if current_iter >= max_iter:
        print(" -> Decision: Maximum iterations reached! Routing to 'publisher' (Guardrail exit) -> END.")
        return "publisher"

    print(" -> Decision: Quality score insufficient (< 8). LOOPING BACK to 'coder' for revisions!")
    return "coder"


# =============================================================================
# 4. ASSEMBLE GRAPH WITH CYCLES
# =============================================================================
def build_refinement_graph():
    r"""
    Graph Topology with Feedback Cycle:

            +--------------+
            |    START     |
            +-------+------+
                    |
                    v
            +-------+------+
    +-----> |    coder     |
    |       +-------+------+
    |               |
    |               v
    |       +-------+------+
    |       |  evaluator   |
    |       +-------+------+
    |               |
    |       [ should_continue? ]
    |         |              |
    |         | Score < 8    | Score >= 8 or Max Iterations
    +---------+              v
                     +-------+------+
                     |  publisher   |
                     +-------+------+
                             |
                             v
                     +-------+------+
                     |     END      |
                     +--------------+
    """
    builder = StateGraph(CodeRefinementState)

    builder.add_node("coder", coder_node)
    builder.add_node("evaluator", evaluator_node)
    builder.add_node("publisher", publisher_node)

    # 1. Flow starts at coder
    builder.add_edge(START, "coder")

    # 2. Coder proceeds to evaluator
    builder.add_edge("coder", "evaluator")

    # 3. Evaluator conditionally routes to 'coder' (loop) or 'publisher' (exit)
    builder.add_conditional_edges(
        "evaluator",
        should_continue,
        {
            "coder": "coder",          # Loop back edge!
            "publisher": "publisher",  # Forward exit edge
        },
    )

    # 4. Publisher ends the graph
    builder.add_edge("publisher", END)

    return builder.compile()


# =============================================================================
# 5. RUN DEMONSTRATION
# =============================================================================
def main():
    print("*" * 70)
    print("PROJECT 007: CONDITIONAL EDGES, DYNAMIC ROUTING & GRAPH CYCLES")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("*" * 70)

    graph = build_refinement_graph()

    task = (
        "Write a robust Python function `parse_date_string(date_str: str) -> dict` "
        "that parses dates in formats YYYY-MM-DD or DD/MM/YYYY, raises ValueError "
        "on malformed strings, and validates leap years."
    )

    initial_state = {
        "task": task,
        "current_code": "",
        "quality_score": 0,
        "critique": "",
        "iteration": 0,
        "max_iterations": 3,
        "cycle_history": ["Session initialized"],
    }

    print(f"Goal: {task}\n")
    final_output = graph.invoke(initial_state)

    print("\n" + "=" * 70)
    print("FINAL REFINED CODE OUTPUT")
    print("=" * 70)
    print(final_output["current_code"])

    print("\n" + "=" * 70)
    print("CYCLE AUDIT TRAIL")
    print("=" * 70)
    for entry in final_output["cycle_history"]:
        print(f" • {entry}")

    print("\n[SUCCESS] Project 007 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()
