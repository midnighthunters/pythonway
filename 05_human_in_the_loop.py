"""
===============================================================================
LANGGRAPH CONCEPT 5: HUMAN-IN-THE-LOOP (HITL) AND BREAKPOINTS
===============================================================================

Why Human-in-the-Loop?
---------------------
Autonomous AI agents are powerful, but enterprise and mission-critical applications
cannot afford unverified actions. Examples:
  - Financial transactions / wire transfers
  - Deleting production database records
  - Sending customer-facing broadcast emails
  - Executing sensitive system commands

LangGraph provides native support for breakpoints:
  `builder.compile(checkpointer=memory, interrupt_before=["action_node"])`
  1. Graph runs until it reaches `action_node`.
  2. Execution PAUSES immediately before `action_node` runs.
  3. The full state is frozen and preserved in the checkpointer.
  4. A human can:
     - Inspect the planned action: `graph.get_state(config)`
     - Edit/Correct the state: `graph.update_state(config, updates)`
     - Resume execution: `graph.invoke(None, config)`
     - Cancel or abort the process

In this lesson:
  1. Agent drafts a financial transaction using Groq LLM.
  2. Graph halts at a breakpoint before money is wired.
  3. Human supervisor reviews the transfer details.
  4. Human modifies the transfer amount and adds manager approval.
  5. Graph resumes and executes the modified transaction safely.
===============================================================================
"""

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from config import get_llm


# =============================================================================
# 1. STATE DEFINITION
# =============================================================================
class TransactionState(TypedDict):
    raw_user_request: str
    recipient: str
    amount: float
    currency: str
    approval_status: str
    manager_note: Optional[str]
    execution_receipt: Optional[str]


# =============================================================================
# 2. NODES
# =============================================================================
def drafter_node(state: TransactionState) -> dict:
    """
    Step 1: Uses Groq LLM to extract structured transaction details
    from natural language user input.
    """
    print("\n--- [NODE 1: DRAFTER] Parsing transfer request with Groq LLM... ---")
    llm = get_llm(temperature=0.0)

    prompt = (
        "Extract the recipient name, numeric amount, and currency code from this text:\n"
        f"'{state['raw_user_request']}'\n\n"
        "Reply in EXACTLY this format (one per line):\n"
        "RECIPIENT: <name>\n"
        "AMOUNT: <numeric value only, e.g. 5000>\n"
        "CURRENCY: <currency code, e.g. USD>"
    )
    res = llm.invoke(prompt)
    lines = res.content.strip().split("\n")

    recipient = "Acme Corp"
    amount = 5000.0
    currency = "USD"

    for line in lines:
        if line.startswith("RECIPIENT:"):
            recipient = line.replace("RECIPIENT:", "").strip()
        elif line.startswith("AMOUNT:"):
            try:
                amount = float(line.replace("AMOUNT:", "").replace("$", "").replace(",", "").strip())
            except ValueError:
                pass
        elif line.startswith("CURRENCY:"):
            currency = line.replace("CURRENCY:", "").strip()

    print(f" -> Prepared Draft: Send {amount} {currency} to {recipient}")
    return {
        "recipient": recipient,
        "amount": amount,
        "currency": currency,
        "approval_status": "PENDING_APPROVAL",
    }


def execute_transaction_node(state: TransactionState) -> dict:
    """
    Step 2: Sensitive Execution Node.
    This node ACTUALLY executes the wire transfer.
    Notice: The graph will PAUSE before this node runs!
    """
    print("\n--- [NODE 2: SENSITIVE EXECUTION] Executing wire transfer... ---")
    status = state.get("approval_status", "UNKNOWN")

    if status != "APPROVED":
        print(" [WARNING] Transaction is NOT approved! Halting execution.")
        return {"execution_receipt": "FAILED: Missing human approval."}

    receipt = (
        f"TXN-SUCCESS | Transferred {state['amount']} {state['currency']} "
        f"to '{state['recipient']}' | Note: {state.get('manager_note', 'None')}"
    )
    print(f" -> [BANK GATEWAY CONFIRMATION]: {receipt}")
    return {
        "approval_status": "EXECUTED",
        "execution_receipt": receipt,
    }


# =============================================================================
# 3. BUILD GRAPH WITH BREAKPOINT (INTERRUPT)
# =============================================================================
def build_hitl_graph():
    builder = StateGraph(TransactionState)

    builder.add_node("drafter", drafter_node)
    builder.add_node("execute_transaction", execute_transaction_node)

    builder.add_edge(START, "drafter")
    builder.add_edge("drafter", "execute_transaction")
    builder.add_edge("execute_transaction", END)

    # In-memory checkpointer is REQUIRED for breakpoints so state can be held
    memory = MemorySaver()

    # CRITICAL: interrupt_before halts graph BEFORE the specified node runs!
    compiled = builder.compile(
        checkpointer=memory,
        interrupt_before=["execute_transaction"],
    )
    return compiled


# =============================================================================
# 4. EXECUTION DEMO WITH HUMAN INTERVENTION
# =============================================================================
def main():
    print("=" * 70)
    print("LANGGRAPH LESSON 5: HUMAN-IN-THE-LOOP & BREAKPOINTS")
    print("=" * 70)

    graph = build_hitl_graph()
    thread_config = {"configurable": {"thread_id": "payment-batch-001"}}

    # Phase 1: User submits a high-value payment request
    user_prompt = "Please wire $50,000 USD to Globex Corporation for infrastructure services."
    print(f"\nIncoming Request: '{user_prompt}'")

    print("\n[PHASE 1] Starting workflow execution...")
    # This will run 'drafter', but STOP before 'execute_transaction'
    graph.invoke(
        {
            "raw_user_request": user_prompt,
            "recipient": "",
            "amount": 0.0,
            "currency": "USD",
            "approval_status": "NEW",
            "manager_note": None,
            "execution_receipt": None,
        },
        config=thread_config,
    )

    # Phase 2: Check the paused state
    print("\n" + "=" * 60)
    print("[PHASE 2] GRAPH PAUSED! INSPECTING CHECKPOINT STATE:")
    print("=" * 60)
    snapshot = graph.get_state(thread_config)
    print(f"Current State Values : {snapshot.values}")
    print(f"Pending Next Node    : {snapshot.next}")  # Should show ('execute_transaction',)

    # Phase 3: Human Manager Review and Intervention
    # The manager notices the requested amount ($50,000) exceeds budget limit.
    # Manager decides to negotiate and adjust amount down to $35,000 and approves it.
    print("\n" + "=" * 60)
    print("[PHASE 3] HUMAN MANAGER INTERVENTION:")
    print("=" * 60)
    print("Manager Action: Adjusting amount to $35,000 and granting approval...")

    graph.update_state(
        thread_config,
        {
            "amount": 35000.0,
            "approval_status": "APPROVED",
            "manager_note": "Approved by Finance Director with $15,000 negotiated discount.",
        },
    )

    # Verify that the state was successfully updated
    updated_snapshot = graph.get_state(thread_config)
    print(f"State after Human Edit: Amount = ${updated_snapshot.values['amount']}, Status = {updated_snapshot.values['approval_status']}")

    # Phase 4: Resume execution!
    # Passing None as the input tells LangGraph to resume from the current checkpoint
    print("\n" + "=" * 60)
    print("[PHASE 4] RESUMING WORKFLOW EXECUTION...")
    print("=" * 60)
    final_output = graph.invoke(None, config=thread_config)

    print("\n--- FINAL WORKFLOW RESULT ---")
    print(f"Status : {final_output['approval_status']}")
    print(f"Receipt: {final_output['execution_receipt']}")


if __name__ == "__main__":
    main()
