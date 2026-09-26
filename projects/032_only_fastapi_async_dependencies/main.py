"""
===============================================================================
PROJECT 032: ASYNC HANDLERS, DEPENDENCY INJECTION & BACKGROUNDTASKS
Stage 1: Pure Fundamentals | Difficulty: 2.5 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
How do production AI APIs handle heavy background processing without stalling
client HTTP requests?

FASTAPI ASYNC CAPABILITIES:
1. Native `async def` Handlers: Asynchronous non-blocking event loops.
2. Inverted Control with `Depends()`: Composable, reusable dependencies (Auth, DB, Context).
3. BackgroundTasks: Returns 200/202 immediately to the user while offloading
   heavy AI synthesis or email dispatch to background threads.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import time
import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, Header, HTTPException, BackgroundTasks, status
from fastapi.testclient import TestClient
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. MODELS & IN-MEMORY STATE
# =============================================================================
class CheckoutRequest(BaseModel):
    customer_id: str = Field(min_length=3)
    drink_name: str
    amount_paid: float = Field(gt=0.0)


class UserContext(BaseModel):
    customer_id: str
    membership_tier: str
    authenticated: bool


AUDIT_LOGS: List[Dict[str, Any]] = []
PROCESSED_RECEIPTS: Dict[str, str] = {}


# =============================================================================
# 2. DEPENDENCY INJECTION ENGINE (Depends)
# =============================================================================
def get_user_context(x_member_id: Optional[str] = Header(default=None)) -> UserContext:
    """Dependency verifying membership headers and injecting context."""
    if not x_member_id:
        return UserContext(customer_id="guest_anon", membership_tier="STANDARD", authenticated=False)

    tier = "VIP" if x_member_id.startswith("VIP-") else "LOYALTY"
    return UserContext(customer_id=x_member_id, membership_tier=tier, authenticated=True)


def get_db_audit_session():
    """Generator dependency simulating database session lifespan and commit."""
    session_id = f"sess_{int(time.time() * 1000) % 10000}"
    # Startup
    yield session_id
    # Teardown commit
    pass


# =============================================================================
# 3. ASYNC BACKGROUND TASK WORKER
# =============================================================================
def background_generate_ai_receipt(order_id: str, customer_id: str, drink: str, amount: float):
    """
    Background worker that runs asynchronously AFTER the HTTP response was sent.
    Uses Groq LLM to synthesize a personalized gratitude note.
    """
    llm = get_llm(temperature=0.4)
    prompt = (
        f"You are the Cozy Coffee Concierge. Customer '{customer_id}' ordered '{drink}' (${amount:.2f}). "
        "Write a warm, 2-sentence personalized thank-you note highlighting a fun flavor fact about the drink."
    )
    ai_note = llm.invoke(prompt).content.strip()

    PROCESSED_RECEIPTS[order_id] = ai_note
    AUDIT_LOGS.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "status": "RECEIPT_DISPATCHED",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    })


# =============================================================================
# 4. FASTAPI APPLICATION & ASYNC ROUTES
# =============================================================================
app = FastAPI(title="Async Dependency & Background Worker Service", version="1.0.0")


@app.post("/checkout", status_code=status.HTTP_202_ACCEPTED)
async def checkout_order(
    req: CheckoutRequest,
    bg_tasks: BackgroundTasks,
    user_ctx: UserContext = Depends(get_user_context),
    db_session: str = Depends(get_db_audit_session),
):
    """
    Async non-blocking endpoint:
    1. Injects UserContext and DB session via Depends.
    2. Enqueues background receipt generation.
    3. Returns 202 Accepted immediately!
    """
    order_id = f"ORD-{int(time.time() * 1000) % 100000:05d}"

    # Enqueue heavy work to background
    bg_tasks.add_task(
        background_generate_ai_receipt,
        order_id=order_id,
        customer_id=user_ctx.customer_id,
        drink=req.drink_name,
        amount=req.amount_paid,
    )

    return {
        "status": "ACCEPTED",
        "order_id": order_id,
        "message": "Order successfully accepted. AI receipt is compiling in background.",
        "user_tier": user_ctx.membership_tier,
        "session_id": db_session,
    }


@app.get("/receipts/{order_id}")
async def get_receipt(order_id: str):
    """Checks status of background-generated receipt."""
    if order_id not in PROCESSED_RECEIPTS:
        return {"order_id": order_id, "status": "PENDING_PROCESSING"}
    return {
        "order_id": order_id,
        "status": "COMPLETED",
        "personalized_note": PROCESSED_RECEIPTS[order_id],
    }


@app.get("/audit")
async def get_audit_trail():
    return {"audit_count": len(AUDIT_LOGS), "records": AUDIT_LOGS}


# =============================================================================
# 5. MAIN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 032: ASYNC HANDLERS, DEPENDENCY INJECTION & BACKGROUNDTASKS")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    client = TestClient(app)

    # 1. VIP Customer Checkout (Trigger Background Task)
    print("\n" + "-" * 75)
    print("1. POST /checkout (With Injected VIP Header)")
    print("-" * 75)
    order_data = {"customer_id": "cust_88", "drink_name": "Ethiopian Yirgacheffe Pour-Over", "amount_paid": 6.50}
    res = client.post("/checkout", json=order_data, headers={"x-member-id": "VIP-ELITE-99"})

    print(f"HTTP Status: {res.status_code} (Immediate 202 Accepted!)")
    body = res.json()
    print(f"Response Payload:\n{body}")
    order_id = body["order_id"]

    # 2. Inspect Background Processing
    print("\n" + "-" * 75)
    print(f"2. GET /receipts/{order_id} (Inspecting Background Worker Execution)")
    print("-" * 75)
    receipt_res = client.get(f"/receipts/{order_id}")
    print(f"Receipt Status: {receipt_res.json()['status']}")
    print(f"AI Personalized Gratitude Note:\n\"{receipt_res.json()['personalized_note']}\"")

    # 3. Audit Verification
    print("\n" + "-" * 75)
    print("3. GET /audit (Verifying Asynchronous Audit Trail)")
    print("-" * 75)
    audit_res = client.get("/audit")
    print(f"Audit Entries: {audit_res.json()['audit_count']}")
    print(audit_res.json()["records"])

    print("\n" + "=" * 75)
    print("[SUCCESS] Project 032 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
