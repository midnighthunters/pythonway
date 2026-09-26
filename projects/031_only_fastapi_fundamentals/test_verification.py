"""
Verification Test Suite for Project 031: FastAPI Fundamentals
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from main import app, OrderCreateRequest, OrderItemRequest


def test_fastapi_endpoints():
    print("Testing FastAPI endpoints using TestClient...")
    client = TestClient(app)

    # 1. Health
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "HEALTHY"

    # 2. Menu
    r = client.get("/menu")
    assert r.status_code == 200
    assert len(r.json()) >= 4

    # 3. Order creation
    payload = {
        "customer_name": "Alice Wonderland",
        "items": [{"menu_item_id": 1, "quantity": 1}],
    }
    r = client.post("/orders", json=payload)
    assert r.status_code == 201
    assert r.json()["customer_name"] == "Alice Wonderland"
    assert r.json()["total"] > 3.50
    print("  [PASSED] Core FastAPI routes and response models verified.")


def test_pydantic_validation_error():
    print("\nTesting Pydantic v2 validation constraints...")
    client = TestClient(app)

    # Empty customer name
    r = client.post("/orders", json={"customer_name": "  ", "items": [{"menu_item_id": 1, "quantity": 1}]})
    assert r.status_code == 422, "Expected 422 Unprocessable Entity for whitespace name"

    # Invalid item ID
    r2 = client.post("/orders", json={"customer_name": "Bob", "items": [{"menu_item_id": 9999, "quantity": 1}]})
    assert r2.status_code == 400, "Expected 400 Bad Request for invalid item ID"
    print("  [PASSED] Pydantic v2 and custom validators cleanly reject invalid inputs.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 031")
    print("=" * 60)
    test_fastapi_endpoints()
    test_pydantic_validation_error()
    print("\n[ALL TESTS PASSED] Project 031 verified successfully!")
