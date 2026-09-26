# Q0931 · OWASP LLM06: Excessive Agency and autonomous destructive tool execution

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | OWASP LLM Top 10 | Hard |

## Question

Explain OWASP LLM06: Excessive Agency, and write Python code implementing an action authorization gate that enforces maximum transaction limits and human approval on destructive tools.

## Answer

Excessive Agency occurs when an LLM agent is granted broader privileges, permissions, or autonomous authority than required. For example, an agent tasked with reading market news is also granted access to a `delete_account` or `transfer_funds` tool without human verification.

The principle of least agency mandates:
1. Separation of read-only tools from state-mutating tools.
2. Hard dollar caps on autonomous execution.
3. Human-In-The-Loop (HITL) step-up confirmation for sensitive operations.

```python
from typing import Dict, Any


class ActionAuthorizationGate:
    def __init__(self, max_autonomous_transfer_usd: float = 10_000.0):
        self.max_auto = max_autonomous_transfer_usd

    def evaluate_tool_execution(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "read_account_balance":
            return {"allowed": True, "requires_hitl": False}

        elif tool_name == "transfer_funds":
            amount = params.get("amount_usd", 0.0)
            if amount > self.max_auto:
                return {
                    "allowed": False,
                    "requires_hitl": True,
                    "reason": f"Transfer amount ${amount} exceeds autonomous ceiling ${self.max_auto}. Human approval required.",
                }
            return {"allowed": True, "requires_hitl": False}

        elif tool_name in ["drop_table", "delete_database", "execute_arbitrary_shell"]:
            return {"allowed": False, "requires_hitl": False, "reason": "Prohibited destructive tool."}

        return {"allowed": False, "requires_hitl": True, "reason": "Unknown tool."}


gate = ActionAuthorizationGate(max_autonomous_transfer_usd=5000.0)

# Read tool: allowed automatically
assert gate.evaluate_tool_execution("read_account_balance", {})["allowed"] is True

# High-value transfer: requires HITL approval
res_large = gate.evaluate_tool_execution("transfer_funds", {"amount_usd": 25000.0})
assert res_large["allowed"] is False
assert res_large["requires_hitl"] is True

# Forbidden destructive tool
res_drop = gate.evaluate_tool_execution("drop_table", {})
assert res_drop["allowed"] is False
assert "Prohibited" in res_drop["reason"]
```

## Likely follow-ups

- How does the principle of least privilege differ from the principle of least agency?
- How do you implement asynchronous human approval workflows in LangGraph?

---

[← Q0930](../../batch_10_ai_security_responsible_ai/0930_owasp_llm05_improper_output_handling_stored_xss_ssrf_and/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0932 →](../../batch_10_ai_security_responsible_ai/0932_owasp_llm07_system_prompt_leakage_and_intellectual_property/README.md)
