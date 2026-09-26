"""
===============================================================================
PROJECT 009: HUMAN-IN-THE-LOOP (HITL), INTERRUPTS & STATE MODIFICATION
Stage 1: Pure Fundamentals | Difficulty: 3.5 / 10 (Intermediate)
===============================================================================

Core Concepts Demonstrated:
1. Human-in-the-Loop (HITL) Gateways: Halting graph execution before sensitive actions.
2. `interrupt_before`: Pausing the graph right before executing specified nodes.
3. State Inspection at Breakpoints: Checking `state.next` and current payload values.
4. Out-of-Band State Mutation: Using `graph.update_state()` to inject human decisions,
   edit proposed parameters, or provide feedback.
5. Resuming Halted Execution: Resuming execution from checkpoint using `graph.invoke(None, config)`.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
import re
from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. STATE DEFINITION
# =============================================================================
class WireTransferState(TypedDict):
    request: str
    recipient: str
    amount: float
    currency: str
    risk_level: str
    human_approved: bool
    human_feedback: str
    execution_status: str
    audit_trail: Annotated[List[str], operator.add]


# =============================================================================
# 2. NODES
# =============================================================================
def proposal_node(state: WireTransferState) -> dict:
    """Extracts wire transfer parameters from user request and calculates risk."""
    print("\n--- [PROPOSAL NODE] Parsing transfer request & assessing financial risk... ---")
    llm = get_llm(temperature=0.0)

    prompt = (
        f"You are a corporate banking assistant. Analyze this wire transfer request:\n"
        f"'{state['request']}'\n\n"
        "Extract recipient name, numeric transfer amount, and 3-letter currency.\n"
        "Respond ONLY in valid JSON format with keys: recipient (str), amount (float), currency (str)."
    )

    response = llm.invoke(prompt)
    raw = response.content.strip()

    # Clean potential markdown fences
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw).strip()

    try:
        data = json.loads(raw)
        recipient = data.get("recipient", "Unknown Recipient")
        amount = float(data.get("amount", 0.0))
        currency = data.get("currency", "USD").upper()
    except Exception:
        recipient = "Default Recipient"
        amount = 5000.0
        currency = "USD"

    risk = "HIGH" if amount >= 10000.0 else "LOW"
    print(f" -> Drafted Transfer : {currency} {amount:,.2f} to {recipient}")
    print(f" -> Risk Assessment  : {risk}")

    return {
        "recipient": recipient,
        "amount": amount,
        "currency": currency,
        "risk_level": risk,
        "audit_trail": [f"Proposal generated: {currency} {amount:,.2f} to {recipient} (Risk: {risk})"],
    }


def execution_gate_node(state: WireTransferState) -> dict:
    """Executes or rejects the wire transfer based on human manager approval."""
    print("\n--- [EXECUTION GATE NODE] Processing finalized transaction... ---")

    approved = state.get("human_approved", False)
    feedback = state.get("human_feedback", "No feedback provided")
    recipient = state.get("recipient")
    amount = state.get("amount", 0.0)
    currency = state.get("currency", "USD")

    if approved:
        tx_id = f"TXN-{abs(hash(recipient + str(amount))) % 1000000:06d}"
        print(f" [AUTHORIZATION CONFIRMED] Wire transfer executed successfully! Transaction ID: {tx_id}")
        return {
            "execution_status": "COMPLETED",
            "audit_trail": [f"Transfer authorized and settled (TX: {tx_id}). Note: {feedback}"],
        }
    else:
        print(f" [AUTHORIZATION DENIED] Transfer aborted! Reason: {feedback}")
        return {
            "execution_status": "REJECTED",
            "audit_trail": [f"Transfer rejected by supervisor. Reason: {feedback}"],
        }


# =============================================================================
# 3. GRAPH COMPILATION WITH HITL INTERRUPT
# =============================================================================
def build_hitl_wire_transfer_graph(checkpointer: MemorySaver = None):
    """
    Compiles the transfer graph with `interrupt_before=['execution_gate']`.
    This guarantees that the graph will stop before executing the financial transfer.
    """
    if checkpointer is None:
        checkpointer = MemorySaver()

    builder = StateGraph(WireTransferState)

    builder.add_node("proposal", proposal_node)
    builder.add_node("execution_gate", execution_gate_node)

    builder.add_edge(START, "proposal")
    builder.add_edge("proposal", "execution_gate")
    builder.add_edge("execution_gate", END)

    # Interrupt right before the execution gate!
    return builder.compile(
        checkpointer=checkpointer,
        interrupt_before=["execution_gate"],
    )


# =============================================================================
# 4. RUN DEMONSTRATION
# =============================================================================
def main():
    print("*" * 70)
    print("PROJECT 009: HUMAN-IN-THE-LOOP (HITL), INTERRUPTS & STATE MUTATION")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("*" * 70)

    memory = MemorySaver()
    graph = build_hitl_wire_transfer_graph(checkpointer=memory)

    # -------------------------------------------------------------------------
    # SCENARIO 1: Manager Inspects, Modifies Amount & Approves
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SCENARIO 1: High-Value Transfer -> Paused -> Modified & Approved")
    print("=" * 70)

    config_1 = {"configurable": {"thread_id": "transfer_thread_001"}}
    initial_request = {
        "request": "Please transfer 25000 USD to Apex Cloud Services for annual server hosting.",
        "recipient": "",
        "amount": 0.0,
        "currency": "",
        "risk_level": "PENDING",
        "human_approved": False,
        "human_feedback": "",
        "execution_status": "DRAFT",
        "audit_trail": ["Transaction initiated by enterprise billing agent"],
    }

    # Step 1: Initial invocation runs until interrupt breakpoint
    print("\n[STEP 1] Starting graph execution...")
    graph.invoke(initial_request, config=config_1)

    # Step 2: Inspect halted state
    snapshot = graph.get_state(config_1)
    print(f"\n[INTERRUPT DETECTED]")
    print(f" -> Next waiting node : {snapshot.next}")
    print(f" -> Proposed Amount   : {snapshot.values['currency']} {snapshot.values['amount']:,.2f}")
    print(f" -> Recipient Target  : {snapshot.values['recipient']}")
    print(f" -> Risk Assessment   : {snapshot.values['risk_level']}")

    # Step 3: Human supervisor applies discount negotiated with vendor ($22,000 instead of $25,000) and approves
    print("\n[STEP 2] Human Supervisor Intervention:")
    print(" -> Action: Applying $3,000 negotiated vendor discount and signing off.")
    graph.update_state(
        config_1,
        values={
            "amount": 22000.0,
            "human_approved": True,
            "human_feedback": "Approved by CFO after applying $3,000 contract discount.",
        },
    )

    # Step 4: Resume execution by passing None
    print("\n[STEP 3] Resuming execution with graph.invoke(None, config)...")
    final_output = graph.invoke(None, config=config_1)

    print("\n[FINAL TRANSACTION STATE]")
    print(f"Status: {final_output['execution_status']}")
    print("Audit History:")
    for note in final_output["audit_trail"]:
        print(f" • {note}")

    # -------------------------------------------------------------------------
    # SCENARIO 2: Manager Rejects Fraudulent / Unauthorized Transfer
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SCENARIO 2: Suspicious Transfer -> Paused -> Supervisor REJECTS")
    print("=" * 70)

    config_2 = {"configurable": {"thread_id": "transfer_thread_002"}}
    suspicious_request = {
        "request": "Urgent wire 90000 USD to Anonymous Offshore Account 49293 immediately.",
        "recipient": "",
        "amount": 0.0,
        "currency": "",
        "risk_level": "PENDING",
        "human_approved": False,
        "human_feedback": "",
        "execution_status": "DRAFT",
        "audit_trail": ["Transaction initiated by external trigger"],
    }

    graph.invoke(suspicious_request, config=config_2)
    snapshot_2 = graph.get_state(config_2)
    print(f"\n[INTERRUPT DETECTED] Next waiting node: {snapshot_2.next}")

    # Supervisor rejects
    print("\n[STEP 2] Supervisor Intervention: REJECTING suspicious transfer.")
    graph.update_state(
        config_2,
        values={
            "human_approved": False,
            "human_feedback": "Flagged as potential unauthorized wire. Compliance team notified.",
        },
    )

    final_output_2 = graph.invoke(None, config=config_2)
    print(f"\n[FINAL TRANSACTION STATE]: {final_output_2['execution_status']}")
    for note in final_output_2["audit_trail"]:
        print(f" • {note}")

    print("\n[SUCCESS] Project 009 executed cleanly end-to-end!")


if __name__ == "__main__":
    main()
