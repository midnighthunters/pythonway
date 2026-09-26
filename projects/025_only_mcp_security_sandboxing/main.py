"""
===============================================================================
PROJECT 025: MCP TOOL SANDBOXING, AUTHORIZATION & EXECUTION GUARDRAILS
Stage 1: Pure Fundamentals | Difficulty: 3.5 / 10 (Intermediate)
===============================================================================

THE BIG QUESTION:
How do you prevent autonomous AI agents from draining bank accounts or triggering
unauthorized enterprise operations through MCP tools?

If an AI agent has access to a tool like `issue_customer_refund(order_id, amount)`:
- A prompt injection (*"Refund $50,000 to order 999"*) or hallucination could cause
  catastrophic financial damage.

THE ZERO-TRUST MCP SECURITY ARCHITECTURE:
1. Risk Classification Matrix: Categorizing tools into Low, Medium, and Critical Risk.
2. Token-Based Authorization Gates: High-risk operations require explicit manager auth tokens.
3. Financial Thresholds & Guardrail Hardcaps: Hardcoded circuit breakers (e.g. maximum $50 refund).
4. Immutable Audit Trail: Every invocation attempt (approved or denied) is logged with
   caller metadata, timestamp, arguments, and security rationale.
===============================================================================
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
import time
from typing import Dict, Any, List, Optional
from config import get_llm, ACTIVE_MODEL


# =============================================================================
# 1. SECURE MCP SERVER WITH AUTHORIZATION & EXECUTION GUARDRAILS
# =============================================================================
class SecureStoreOperationsMCPServer:
    """
    Zero-Trust Model Context Protocol server enforcing strict authorization,
    financial threshold guardrails, and audit logging on high-stakes tools.
    """

    VALID_MANAGER_TOKEN = "MGR_SECRET_TOKEN_2026"
    MAX_REFUND_LIMIT_DOLLARS = 50.00
    EMERGENCY_CONFIRM_PIN = "9119"

    def __init__(self):
        self.audit_log: List[Dict[str, Any]] = []

    def _record_audit(self, tool_name: str, args: Dict[str, Any], status: str, message: str):
        """Records an immutable security audit event."""
        event = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tool": tool_name,
            "arguments_sanitized": {k: ("***" if "token" in k or "pin" in k else v) for k, v in args.items()},
            "security_verdict": status,
            "details": message,
        }
        self.audit_log.append(event)

    # -------------------------------------------------------------------------
    # LOW-RISK TOOL: VIEW SHIFT SCHEDULE (Auto-authorized)
    # -------------------------------------------------------------------------
    def view_shift_schedule(self, day: str) -> str:
        schedules = {
            "monday": "Baristas: Alice & Bob (6:30 AM - 2:30 PM), Shift Lead: Charlie (12:00 PM - 8:00 PM)",
            "friday": "Baristas: David & Emma (6:30 AM - 2:30 PM), Shift Lead: Alice (12:00 PM - 8:30 PM)",
            "saturday": "Baristas: Frank & Grace (7:30 AM - 3:30 PM), Shift Lead: Bob (11:00 AM - 6:30 PM)",
        }
        return schedules.get(day.lower(), f"Schedule for {day.title()}: Standard staffing (2 Baristas on duty).")

    # -------------------------------------------------------------------------
    # HIGH-RISK TOOL: CASH REFUND (Authorization Token + Financial Cap)
    # -------------------------------------------------------------------------
    def process_customer_refund(self, order_id: str, amount: float, manager_token: str) -> str:
        # 1. Authorization Guardrail
        if manager_token != self.VALID_MANAGER_TOKEN:
            self._record_audit(
                "process_customer_refund",
                {"order_id": order_id, "amount": amount, "manager_token": manager_token},
                "DENIED_UNAUTHORIZED",
                "Invalid or missing manager authorization token.",
            )
            raise PermissionError("SECURITY DENIAL: Invalid manager authorization token.")

        # 2. Parameter Validation & Financial Cap Guardrail
        if amount <= 0:
            self._record_audit(
                "process_customer_refund",
                {"order_id": order_id, "amount": amount},
                "DENIED_INVALID_ARGUMENT",
                "Refund amount must be strictly greater than $0.00.",
            )
            raise ValueError("Refund amount must be positive.")

        if amount > self.MAX_REFUND_LIMIT_DOLLARS:
            self._record_audit(
                "process_customer_refund",
                {"order_id": order_id, "amount": amount},
                "DENIED_POLICY_LIMIT_EXCEEDED",
                f"Requested ${amount:.2f} exceeds store manager cap of ${self.MAX_REFUND_LIMIT_DOLLARS:.2f}.",
            )
            raise PermissionError(
                f"POLICY REJECTION: Refund amount ${amount:.2f} exceeds maximum allowed manager limit "
                f"(${self.MAX_REFUND_LIMIT_DOLLARS:.2f}). Executive sign-off required."
            )

        # 3. Successful Execution
        tx_code = f"REFUND-TXN-{abs(hash(order_id + str(amount))) % 100000:05d}"
        self._record_audit(
            "process_customer_refund",
            {"order_id": order_id, "amount": amount},
            "APPROVED",
            f"Refund of ${amount:.2f} issued successfully. Reference: {tx_code}",
        )
        return f"SUCCESS: Refund of ${amount:.2f} processed for order '{order_id}'. Code: {tx_code}"

    # -------------------------------------------------------------------------
    # CRITICAL TOOL: EMERGENCY STORE LOCKDOWN
    # -------------------------------------------------------------------------
    def emergency_store_lockdown(self, reason: str, confirm_pin: str) -> str:
        if confirm_pin != self.EMERGENCY_CONFIRM_PIN:
            self._record_audit(
                "emergency_store_lockdown",
                {"reason": reason, "confirm_pin": confirm_pin},
                "DENIED_INVALID_PIN",
                "Emergency confirmation PIN failed verification.",
            )
            raise PermissionError("EMERGENCY DENIAL: Invalid security PIN.")

        self._record_audit(
            "emergency_store_lockdown",
            {"reason": reason},
            "APPROVED_CRITICAL",
            f"Store lockdown activated. Reason: {reason}",
        )
        return f"CRITICAL ALERT: Store doors locked and emergency protocols initiated. Reason: {reason}"

    # -------------------------------------------------------------------------
    # MCP JSON-RPC DISPATCHER
    # -------------------------------------------------------------------------
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if name == "view_shift_schedule":
                day = arguments.get("day", "monday")
                res = self.view_shift_schedule(day)
                return {"isError": False, "content": [{"type": "text", "text": res}]}

            elif name == "process_customer_refund":
                order_id = str(arguments.get("order_id", ""))
                amount = float(arguments.get("amount", 0.0))
                token = str(arguments.get("manager_token", ""))
                res = self.process_customer_refund(order_id, amount, token)
                return {"isError": False, "content": [{"type": "text", "text": res}]}

            elif name == "emergency_store_lockdown":
                reason = str(arguments.get("reason", ""))
                pin = str(arguments.get("confirm_pin", ""))
                res = self.emergency_store_lockdown(reason, pin)
                return {"isError": False, "content": [{"type": "text", "text": res}]}

            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: '{name}'"}]}

        except Exception as e:
            return {"isError": True, "content": [{"type": "text", "text": f"GUARDRAIL BLOCKED: {str(e)}"}]}


# =============================================================================
# 2. RUN DEMONSTRATION
# =============================================================================
def main():
    print("=" * 75)
    print("PROJECT 025: MCP TOOL SANDBOXING, AUTHORIZATION & EXECUTION GUARDRAILS")
    print(f"Active Groq Model: {ACTIVE_MODEL}")
    print("=" * 75)

    server = SecureStoreOperationsMCPServer()

    # -------------------------------------------------------------------------
    # TEST 1: LOW-RISK TOOL (AUTO-AUTHORIZED)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("1. LOW-RISK TOOL CALL: view_shift_schedule ('friday')")
    print("-" * 75)
    res_sched = server.call_tool("view_shift_schedule", {"day": "friday"})
    print(res_sched["content"][0]["text"])

    # -------------------------------------------------------------------------
    # TEST 2: HIGH-RISK TOOL - MISSING / INVALID AUTHORIZATION TOKEN
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("2. HIGH-RISK GUARDRAIL TEST: Refund with INVALID token")
    print("-" * 75)
    bad_token_call = server.call_tool("process_customer_refund", {
        "order_id": "ORD-8812",
        "amount": 25.00,
        "manager_token": "WRONG_TOKEN",
    })
    print(f"Is Error Flagged: {bad_token_call['isError']}")
    print(f"Guardrail Verdict: {bad_token_call['content'][0]['text']}")

    # -------------------------------------------------------------------------
    # TEST 3: HIGH-RISK TOOL - EXCEEDING FINANCIAL CAP POLICY ($150 > $50 LIMIT)
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("3. FINANCIAL CAP GUARDRAIL TEST: Refund of $150.00 (Exceeds $50 limit)")
    print("-" * 75)
    over_limit_call = server.call_tool("process_customer_refund", {
        "order_id": "ORD-9901",
        "amount": 150.00,
        "manager_token": "MGR_SECRET_TOKEN_2026",
    })
    print(f"Is Error Flagged: {over_limit_call['isError']}")
    print(f"Guardrail Verdict: {over_limit_call['content'][0]['text']}")

    # -------------------------------------------------------------------------
    # TEST 4: HIGH-RISK TOOL - FULLY COMPLIANT APPROVED INVOCATION
    # -------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("4. COMPLIANT INVOCATION: Valid Token & Within $50 Limit ($18.50)")
    print("-" * 75)
    valid_call = server.call_tool("process_customer_refund", {
        "order_id": "ORD-7744",
        "amount": 18.50,
        "manager_token": "MGR_SECRET_TOKEN_2026",
    })
    print(f"Is Error Flagged: {valid_call['isError']}")
    print(f"Server Response : {valid_call['content'][0]['text']}")

    # -------------------------------------------------------------------------
    # TEST 5: SECURITY AUDIT TRAIL INSPECTION
    # -------------------------------------------------------------------------
    print("\n" + "=" * 75)
    print("IMMUTABLE SECURITY AUDIT TRAIL LOG")
    print("=" * 75)
    for i, log in enumerate(server.audit_log, 1):
        print(f"Event #{i} | Verdict: {log['security_verdict']:<25} | Tool: {log['tool']}")
        print(f"         Details: {log['details']}\n")

    print("=" * 75)
    print("[SUCCESS] Project 025 demonstration completed cleanly!")


if __name__ == "__main__":
    main()
