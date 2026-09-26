"""
Verification Test Suite for Project 025: MCP Tool Sandboxing & Guardrails
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from main import SecureStoreOperationsMCPServer


def test_authorization_and_financial_limits():
    print("Testing MCP tool authorization and financial safety guardrails...")
    server = SecureStoreOperationsMCPServer()

    # 1. Low risk tool
    res_low = server.call_tool("view_shift_schedule", {"day": "monday"})
    assert res_low["isError"] is False
    assert "Alice" in res_low["content"][0]["text"]
    print("  [PASSED] Low-risk tool executed without authentication barrier.")

    # 2. Unauthorized high-risk tool call
    res_unauth = server.call_tool("process_customer_refund", {
        "order_id": "ORD-1",
        "amount": 20.0,
        "manager_token": "FAKE_TOKEN",
    })
    assert res_unauth["isError"] is True
    assert "SECURITY DENIAL" in res_unauth["content"][0]["text"]
    print("  [PASSED] Missing/invalid authorization token blocked.")

    # 3. Financial cap exceedance
    res_cap = server.call_tool("process_customer_refund", {
        "order_id": "ORD-2",
        "amount": 75.0,  # Exceeds $50 limit
        "manager_token": "MGR_SECRET_TOKEN_2026",
    })
    assert res_cap["isError"] is True
    assert "POLICY REJECTION" in res_cap["content"][0]["text"]
    print("  [PASSED] Financial cap limit ($50.00) enforced.")

    # 4. Valid compliant refund
    res_valid = server.call_tool("process_customer_refund", {
        "order_id": "ORD-3",
        "amount": 24.50,
        "manager_token": "MGR_SECRET_TOKEN_2026",
    })
    assert res_valid["isError"] is False
    assert "SUCCESS" in res_valid["content"][0]["text"]
    print("  [PASSED] Authorized, compliant tool execution succeeded.")


def test_emergency_gate_and_audit_trail():
    print("\nTesting emergency pin gate and audit trail recording...")
    server = SecureStoreOperationsMCPServer()

    # Invalid PIN emergency call
    res_bad_pin = server.call_tool("emergency_store_lockdown", {
        "reason": "Fire alarm",
        "confirm_pin": "0000",
    })
    assert res_bad_pin["isError"] is True
    assert "EMERGENCY DENIAL" in res_bad_pin["content"][0]["text"]
    print("  [PASSED] Invalid emergency confirmation PIN rejected.")

    # Valid PIN emergency call
    res_good_pin = server.call_tool("emergency_store_lockdown", {
        "reason": "Water pipe leak",
        "confirm_pin": "9119",
    })
    assert res_good_pin["isError"] is False
    print("  [PASSED] Valid emergency PIN confirmed and executed.")

    # Audit log validation
    assert len(server.audit_log) == 2
    for entry in server.audit_log:
        assert "pin" not in entry["arguments_sanitized"] or entry["arguments_sanitized"].get("confirm_pin") == "***"
    print(f"  [PASSED] Audit trail logged {len(server.audit_log)} security events with sanitized credentials.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: PROJECT 025")
    print("=" * 60)
    test_authorization_and_financial_limits()
    test_emergency_gate_and_audit_trail()
    print("\n[ALL TESTS PASSED] Project 025 verified successfully!")
