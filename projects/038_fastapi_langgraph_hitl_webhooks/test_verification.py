"""
Test verification suite for Project 038: FastAPI + LangGraph HITL Guardrail Webhook API
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from main import app


def test_low_risk_auto_approval():
    client = TestClient(app)
    res = client.post(
        "/refunds/submit",
        json={"order_id": "ORD-TEST-01", "customer_name": "Test User", "amount": 25.0, "reason": "Spilled drink"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "AUTO_COMPLETED"
    assert data["payout_reference"] is not None


def test_high_risk_pause_and_approval_webhook():
    client = TestClient(app)
    order_id = "ORD-TEST-HIGH-99"

    # Step 1: Submit high value refund
    res = client.post(
        "/refunds/submit",
        json={"order_id": order_id, "customer_name": "VIP Customer", "amount": 120.0, "reason": "Event cancel"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "PENDING_HUMAN_APPROVAL"
    assert "execute_manual_payout" in data["next_step"]

    # Step 2: Inspect paused state
    inspect_res = client.get(f"/webhook/approval/{order_id}")
    assert inspect_res.status_code == 200
    inspect_data = inspect_res.json()
    assert "execute_manual_payout" in inspect_data["paused_at"]

    # Step 3: Approve via webhook
    webhook_res = client.post(
        f"/webhook/approval/{order_id}",
        json={"decision": "APPROVED", "reviewer": "Manager Jane", "notes": "Approved after contract review"},
    )
    assert webhook_res.status_code == 200
    wh_data = webhook_res.json()
    assert wh_data["status"] == "REFUND_COMPLETED"
    assert wh_data["payout_reference"] is not None
    assert wh_data["ai_confirmation"] is not None
    assert len(wh_data["ai_confirmation"]) > 0


def test_high_risk_rejection_webhook():
    client = TestClient(app)
    order_id = "ORD-TEST-REJECT-88"

    res = client.post(
        "/refunds/submit",
        json={"order_id": order_id, "customer_name": "Suspicious User", "amount": 80.0, "reason": "No receipt"},
    )
    assert res.status_code == 200
    assert res.json()["status"] == "PENDING_HUMAN_APPROVAL"

    webhook_res = client.post(
        f"/webhook/approval/{order_id}",
        json={"decision": "REJECTED", "reviewer": "Security Lead", "notes": "Fraudulent claim"},
    )
    assert webhook_res.status_code == 200
    assert webhook_res.json()["status"] == "REFUND_REJECTED"


def test_nonexistent_approval_404():
    client = TestClient(app)
    res = client.get("/webhook/approval/NON_EXISTENT_ORD")
    assert res.status_code == 404


if __name__ == "__main__":
    test_low_risk_auto_approval()
    test_high_risk_pause_and_approval_webhook()
    test_high_risk_rejection_webhook()
    test_nonexistent_approval_404()
    print("Project 038: All verification tests PASSED successfully!")
