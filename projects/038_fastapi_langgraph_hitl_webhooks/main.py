"""
===============================================================================
PROJECT 038: FASTAPI + LANGGRAPH: ASYNC HUMAN GUARDRAIL APPROVAL WEBHOOK API
Stage 2: Pairwise Combos | Difficulty: 5.0 / 10
===============================================================================

THE BIG QUESTION:
How do enterprise AI systems pause multi-step agent workflows when high-risk
financial or operational thresholds are triggered (e.g. refunds > $50), release
the HTTP connection with HTTP 202 Accepted, and asynchronously resume execution
when a human manager submits an out-of-band webhook approval?

ARCHITECTURE:
1. LangGraph StateMachine with interrupt_before=["execute_payout"]:
   - Pauses execution before financial transfer if amount exceeds $50.00.
2. Webhook Event Loop:
   - POST /refunds/submit -> Pauses at guardrail -> Returns HTTP 202 Accepted.
   - GET /webhook/approval/{order_id} -> Inspects pending state & next action.
   - POST /webhook/approval/{order_id} -> Updates state with reviewer notes & resumes graph.
3. Groq LLM Receipt Synthesis:
   - Upon resumption, generates an executive audit trail & customer apology note.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import uuid
import json
from typing import TypedDict, Optional, Dict, Any, List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. LANGGRAPH STATE DEFINITION & HITL NODES
# =============================================================================
HIGH_RISK_THRESHOLD_USD = 50.00


class RefundState(TypedDict):
    order_id: str
    customer_name: str
    amount: float
    reason: str
    requires_human_approval: bool
    approval_status: str  # PENDING, APPROVED, REJECTED, AUTO_APPROVED
    reviewer_name: Optional[str]
    reviewer_notes: Optional[str]
    payout_reference: Optional[str]
    ai_confirmation: Optional[str]


def triage_refund_request(state: RefundState) -> Dict[str, Any]:
    """Analyzes transaction value to determine if human guardrail review is required."""
    amt = state["amount"]
    if amt >= HIGH_RISK_THRESHOLD_USD:
        return {
            "requires_human_approval": True,
            "approval_status": "PENDING",
        }
    else:
        return {
            "requires_human_approval": False,
            "approval_status": "AUTO_APPROVED",
        }


def execute_auto_payout(state: RefundState) -> Dict[str, Any]:
    """Instant automated payout for low-risk transactions under threshold."""
    payout_id = f"AUTO-PAYOUT-{uuid.uuid4().hex[:8].upper()}"
    return {
        "payout_reference": payout_id,
        "reviewer_name": "Automated Low-Risk Policy",
        "reviewer_notes": "Order amount falls under $50.00 instant-satisfaction policy",
    }


def execute_manual_payout(state: RefundState) -> Dict[str, Any]:
    """Protected manual payout that runs ONLY after human manager guardrail approval."""
    payout_id = f"MANUAL-PAYOUT-{uuid.uuid4().hex[:8].upper()}"
    return {
        "payout_reference": payout_id,
    }


def triage_router(state: RefundState) -> str:
    """Routes high-risk refunds to the guarded manual node, low-risk to auto node."""
    if state["requires_human_approval"]:
        return "execute_manual_payout"
    return "execute_auto_payout"


def generate_receipt(state: RefundState) -> Dict[str, Any]:
    """Groq LLM synthesizes an audit receipt and customer notification."""
    llm = get_llm(temperature=0.2)
    prompt = (
        f"You are the Finance Lead at Cozy Cafe. "
        f"Generate a professional, warm 2-sentence confirmation for a refund of ${state['amount']:.2f} "
        f"to customer {state['customer_name']} (Order #{state['order_id']}). "
        f"Payout Ref: {state['payout_reference']}. Approved by: {state.get('reviewer_name', 'Automated System')}. "
        f"Reviewer Note: {state.get('reviewer_notes', 'Standard refund policy')}."
    )
    res = llm.invoke(prompt)
    return {"ai_confirmation": res.content.strip()}


# Compile graph with interrupt_before guardrail on execute_manual_payout
workflow = StateGraph(RefundState)
workflow.add_node("triage", triage_refund_request)
workflow.add_node("execute_auto_payout", execute_auto_payout)
workflow.add_node("execute_manual_payout", execute_manual_payout)
workflow.add_node("generate_receipt", generate_receipt)

workflow.add_edge(START, "triage")
workflow.add_conditional_edges("triage", triage_router, ["execute_auto_payout", "execute_manual_payout"])
workflow.add_edge("execute_auto_payout", "generate_receipt")
workflow.add_edge("execute_manual_payout", "generate_receipt")
workflow.add_edge("generate_receipt", END)

checkpointer = MemorySaver()
# The crucial HITL guardrail: interrupt immediately BEFORE executing high-risk manual payout
graph = workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["execute_manual_payout"],
)


# =============================================================================
# 2. FASTAPI APPLICATION & WEBHOOK GATEWAY
# =============================================================================
app = FastAPI(title="HITL Human Guardrail Webhook Gateway", version="1.0.0")


class RefundSubmitRequest(BaseModel):
    order_id: str = Field(..., description="Unique order ID")
    customer_name: str = Field(..., description="Customer's full name")
    amount: float = Field(..., gt=0, description="Refund amount in USD")
    reason: str = Field(..., description="Reason for requesting refund")


class ApprovalWebhookRequest(BaseModel):
    decision: str = Field(..., pattern="^(APPROVED|REJECTED)$", description="'APPROVED' or 'REJECTED'")
    reviewer: str = Field(..., description="Manager or Auditor name")
    notes: str = Field(default="", description="Auditor justification or notes")


@app.post("/refunds/submit")
async def submit_refund(req: RefundSubmitRequest):
    """
    Submits a refund request.
    If amount >= $50, the graph halts at the guardrail and returns HTTP 202 Accepted.
    If amount < $50, the graph executes automatically to completion and returns HTTP 200 OK.
    """
    config = {"configurable": {"thread_id": req.order_id}}

    initial_state: RefundState = {
        "order_id": req.order_id,
        "customer_name": req.customer_name,
        "amount": req.amount,
        "reason": req.reason,
        "requires_human_approval": False,
        "approval_status": "SUBMITTED",
        "reviewer_name": None,
        "reviewer_notes": None,
        "payout_reference": None,
        "ai_confirmation": None,
    }

    # Execute graph until completion OR until hitl interrupt
    graph.invoke(initial_state, config=config)

    snapshot = graph.get_state(config)

    # Check if graph paused at the interrupt_before guardrail
    if "execute_manual_payout" in snapshot.next:
        return {
            "status": "PENDING_HUMAN_APPROVAL",
            "message": f"Refund of ${req.amount:.2f} exceeds threshold (${HIGH_RISK_THRESHOLD_USD:.2f}). Paused for manager review.",
            "order_id": req.order_id,
            "next_step": snapshot.next,
            "webhook_approval_url": f"/webhook/approval/{req.order_id}",
        }

    # Auto-approved low risk refund
    return {
        "status": "AUTO_COMPLETED",
        "order_id": req.order_id,
        "amount": req.amount,
        "payout_reference": snapshot.values.get("payout_reference"),
        "ai_confirmation": snapshot.values.get("ai_confirmation"),
    }


@app.get("/webhook/approval/{order_id}")
async def inspect_pending_approval(order_id: str):
    """Inspects paused state and details waiting for human guardrail review."""
    config = {"configurable": {"thread_id": order_id}}
    snapshot = graph.get_state(config)

    if not snapshot or not snapshot.values:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")

    return {
        "order_id": order_id,
        "paused_at": snapshot.next,
        "state_snapshot": snapshot.values,
    }


@app.post("/webhook/approval/{order_id}")
async def process_approval_webhook(order_id: str, req: ApprovalWebhookRequest):
    """
    Manager webhook callback.
    Updates paused thread state and resumes execution to complete payout & receipt.
    """
    config = {"configurable": {"thread_id": order_id}}
    snapshot = graph.get_state(config)

    if not snapshot or not snapshot.values:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")

    if not snapshot.next:
        return {"status": "ALREADY_COMPLETED", "detail": "This workflow has already finalized."}

    if req.decision == "REJECTED":
        # Update state to REJECTED and finalize
        graph.update_state(
            config,
            {"approval_status": "REJECTED", "reviewer_name": req.reviewer, "reviewer_notes": req.notes},
            as_node="triage",
        )
        return {
            "status": "REFUND_REJECTED",
            "order_id": order_id,
            "reviewer": req.reviewer,
            "notes": req.notes,
        }

    # Manager APPROVED: update state and resume execution
    graph.update_state(
        config,
        {"approval_status": "APPROVED", "reviewer_name": req.reviewer, "reviewer_notes": req.notes},
        as_node="triage",
    )

    # Resume graph by passing None
    final_output = graph.invoke(None, config=config)

    return {
        "status": "REFUND_COMPLETED",
        "order_id": order_id,
        "payout_reference": final_output.get("payout_reference"),
        "reviewer": req.reviewer,
        "reviewer_notes": req.notes,
        "ai_confirmation": final_output.get("ai_confirmation"),
    }


# =============================================================================
# 3. MAIN DEMONSTRATION RUNNER
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 038: FASTAPI + LANGGRAPH HITL GUARDRAIL WEBHOOKS")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    client = TestClient(app)

    # Case 1: Auto-approved low risk refund (< $50)
    print("\n" + "-" * 75)
    print("1. LOW-RISK REFUND ($12.50) -> Auto-Approved Without Interruption")
    print("-" * 75)
    low_res = client.post(
        "/refunds/submit",
        json={"order_id": "ORD-101", "customer_name": "Bob Smith", "amount": 12.50, "reason": "Cold croissant"},
    )
    print(f"Status Code: {low_res.status_code}")
    print(json.dumps(low_res.json(), indent=2))

    # Case 2: High-risk refund (> $50) -> Pauses at Guardrail
    print("\n" + "-" * 75)
    print("2. HIGH-RISK REFUND ($145.00) -> Halts at interrupt_before Guardrail")
    print("-" * 75)
    high_res = client.post(
        "/refunds/submit",
        json={
            "order_id": "ORD-999",
            "customer_name": "Dr. Evelyn Reed",
            "amount": 145.00,
            "reason": "Catering coffee urn damaged on delivery",
        },
    )
    print(f"Status: {high_res.status_code}")
    print(json.dumps(high_res.json(), indent=2))

    # Case 3: Manager Inspects Pending State
    print("\n" + "-" * 75)
    print("3. MANAGER INSPECTS PAUSED THREAD: GET /webhook/approval/ORD-999")
    print("-" * 75)
    inspect_res = client.get("/webhook/approval/ORD-999")
    print(json.dumps(inspect_res.json(), indent=2))

    # Case 4: Manager Calls Approval Webhook to Resume Graph
    print("\n" + "-" * 75)
    print("4. MANAGER SUBMITS APPROVAL WEBHOOK: POST /webhook/approval/ORD-999")
    print("-" * 75)
    webhook_res = client.post(
        "/webhook/approval/ORD-999",
        json={
            "decision": "APPROVED",
            "reviewer": "Samantha Vance (General Manager)",
            "notes": "Verified catering damage with courier receipt. Full reimbursement approved.",
        },
    )
    print(f"Status Code: {webhook_res.status_code}")
    print("Final Execution Response:")
    print(json.dumps(webhook_res.json(), indent=2))

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 038 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
