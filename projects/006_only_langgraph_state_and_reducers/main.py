"""
===============================================================================
PROJECT 006: STATEGRAPH FUNDAMENTALS & REDUCERS (EASY BEGINNER EXAMPLE)
Stage 1: Pure Fundamentals | Difficulty: 2.0 / 10
===============================================================================

Topic: "Trip Planner & Packing Assistant"

THE CORE CONCEPT IN 30 SECONDS:
In LangGraph, all nodes share a single state (think of it as a shared notebook).

1. DEFAULT BEHAVIOR (Overwrite):
   If Node 1 writes `status = "Packing Clothes"`, and Node 2 writes `status = "Packing Tech"`,
   Node 2 OVERWRITES Node 1. The old status is gone. That's standard Python dictionary behavior.

2. REDUCER BEHAVIOR (Append / Accumulate with `Annotated`):
   What about the packing list?
   If Node 1 adds `["Jacket"]`, and Node 2 adds `["Charger"]`, we DO NOT want Node 2 to wipe out
   the jacket! We want BOTH items!
   That is why we use: `Annotated[List[str], operator.add]`.
   It tells LangGraph: "Don't overwrite this! Use `+` to APPEND new items to existing ones!"
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
# 1. STATE DEFINITION (The "Shared Notebook")
# =============================================================================
# TypedDict means this is a regular Python dictionary with type hints.
# You don't need __init__ or methods. It is just a dictionary!
class VacationPlanState(TypedDict):
    # FIELD 1: Overwrite (Regular field)
    # Each node replaces whatever was there before.
    destination: str
    current_status: str

    # FIELD 2: Reducer (operator.add on Lists = APPEND)
    # When a node returns items here, LangGraph does: existing_list + new_list
    packing_list: Annotated[List[str], operator.add]

    # FIELD 3: Reducer (operator.add on Numbers = SUM)
    # When a node returns a number here, LangGraph does: existing_budget + new_budget
    estimated_cost: Annotated[int, operator.add]


# =============================================================================
# 2. NODES (The Workers who read and write to the notebook)
# =============================================================================
def clothing_node(state: VacationPlanState) -> dict:
    """
    Worker 1: Recommends clothing based on the destination.
    """
    dest = state["destination"]
    print(f"\n[Step 1: Clothing Agent] Planning outfits for {dest}...")

    # Ask LLM for 2 essential clothing items
    llm = get_llm(temperature=0.0)
    prompt = (
        f"Give exactly 2 essential clothing items to pack for a trip to {dest}. "
        "Return ONLY the 2 items separated by a comma. Example: Rain jacket, Comfortable walking shoes"
    )
    response = llm.invoke(prompt)
    items = [item.strip() for item in response.content.split(",") if item.strip()]

    # Return partial updates. LangGraph will merge these into the state!
    return {
        "current_status": "Clothing planned",  # OVERWRITES previous status
        "packing_list": items,                 # APPENDS to packing_list!
        "estimated_cost": 150,                 # ADDS 150 to total cost!
    }


def electronics_node(state: VacationPlanState) -> dict:
    """
    Worker 2: Recommends electronics and travel gear.
    """
    dest = state["destination"]
    print(f"\n[Step 2: Electronics Agent] Adding travel tech for {dest}...")

    tech_items = ["Universal plug adapter", "Portable power bank"]

    return {
        "current_status": "Electronics added",  # OVERWRITES previous status
        "packing_list": tech_items,             # APPENDS! (Does NOT erase clothing!)
        "estimated_cost": 50,                   # ADDS 50 to total cost!
    }


def documents_node(state: VacationPlanState) -> dict:
    """
    Worker 3: Recommends critical travel documents.
    """
    print(f"\n[Step 3: Document Agent] Checking essential travel documents...")

    docs = ["Passport / National ID", "Travel insurance card"]

    return {
        "current_status": "Ready to travel!",  # OVERWRITES previous status
        "packing_list": docs,                  # APPENDS! (Does NOT erase anything!)
        "estimated_cost": 25,                  # ADDS 25 to total cost!
    }


# =============================================================================
# 3. BUILD THE GRAPH (Connecting the steps)
# =============================================================================
def build_vacation_graph():
    """
    Workflow:
      START -> clothing_node -> electronics_node -> documents_node -> END
    """
    builder = StateGraph(VacationPlanState)

    # Add the 3 workers
    builder.add_node("clothing", clothing_node)
    builder.add_node("electronics", electronics_node)
    builder.add_node("documents", documents_node)

    # Connect them sequentially
    builder.add_edge(START, "clothing")
    builder.add_edge("clothing", "electronics")
    builder.add_edge("electronics", "documents")
    builder.add_edge("documents", END)

    return builder.compile()


# =============================================================================
# 4. RUN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 70)
    print("PROJECT 006: STATE & REDUCERS MADE SIMPLE")
    print("Example: Automatic Vacation Trip Planner")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 70)

    # 1. Compile the graph
    app = build_vacation_graph()

    # 2. Define the initial state (the starting page of our notebook)
    initial_state = {
        "destination": "Tokyo, Japan",
        "current_status": "Just started",
        "packing_list": [],  # Starts empty
        "estimated_cost": 0, # Starts at $0
    }

    print("\n[INITIAL STATE BEFORE GRAPH RUNS]:")
    print(f"  • destination    : {initial_state['destination']}")
    print(f"  • current_status : {initial_state['current_status']}")
    print(f"  • packing_list   : {initial_state['packing_list']} (0 items)")
    print(f"  • estimated_cost : ${initial_state['estimated_cost']}")

    # 3. Stream the graph to watch how the state updates step-by-step
    print("\n" + "-" * 70)
    print("EXECUTING WORKFLOW STEP-BY-STEP:")
    print("-" * 70)

    final_state = app.invoke(initial_state)

    # 4. Display the final result
    print("\n" + "=" * 70)
    print("FINAL STATE AFTER ALL NODES COMPLETED:")
    print("=" * 70)
    print(f"  • Destination    : {final_state['destination']}")
    print(f"  • Final Status   : {final_state['current_status']} (Notice: OVERWRITTEN from 'Just started')")
    print(f"  • Estimated Cost : ${final_state['estimated_cost']} (Notice: 150 + 50 + 25 = $225 SUMMED)")
    print(f"\n  • Full Packing List ({len(final_state['packing_list'])} items accumulated without overwriting!):")
    for i, item in enumerate(final_state["packing_list"], 1):
        print(f"      {i}. {item}")

    print("\n" + "=" * 70)
    print("KEY LESSON:")
    print("1. 'current_status' used default behavior: each step replaced the last text.")
    print("2. 'packing_list' used operator.add: each step APPENDED its items to the list.")
    print("3. 'estimated_cost' used operator.add on numbers: each step ADDED to the sum.")
    print("=" * 70)
    print("\n[SUCCESS] Project 006 demonstration finished cleanly!")


if __name__ == "__main__":
    main()
