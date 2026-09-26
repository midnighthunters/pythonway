"""
Verification Test Suite for Project 032: FastAPI Async Dependencies & BackgroundTasks
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from main import app, get_user_context, UserContext


def test_dependency_injection():
    print("Testing Depends(get_user_context) resolution...")
    # VIP case
    ctx_vip = get_user_context("VIP-123")
    assert ctx_vip.membership_tier == "VIP"
    assert ctx_vip.authenticated

    # Anonymous case
    ctx_anon = get_user_context(None)
    assert ctx_anon.membership_tier == "STANDARD"
    assert not ctx_anon.authenticated
    print("  [PASSED] Dependency injection accurately infers user tier from headers.")


def test_background_task_execution():
    print("\nTesting BackgroundTasks execution on /checkout...")
    client = TestClient(app)

    payload = {"customer_id": "test_usr", "drink_name": "Iced Matcha", "amount_paid": 5.00}
    res = client.post("/checkout", json=payload)
    assert res.status_code == 202
    data = res.json()
    order_id = data["order_id"]

    # In TestClient, background tasks run synchronously before returning
    rec = client.get(f"/receipts/{order_id}")
    assert rec.status_code == 200
    assert rec.json()["status"] == "COMPLETED"
    assert len(rec.json()["personalized_note"]) > 10
    print("  [PASSED] Background task ran cleanly and produced AI receipt.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 032")
    print("=" * 60)
    test_dependency_injection()
    test_background_task_execution()
    print("\n[ALL TESTS PASSED] Project 032 verified successfully!")
