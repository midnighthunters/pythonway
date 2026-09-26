# Q0698 · PII scrubbing and data loss prevention at tool gateways

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP and A2A security | Hard |

## Question

Implement a gateway filter that intercepts MCP tool call arguments, inspects them for sensitive bank account patterns, and blocks calls that violate data governance policies.

## Answer

```python
import re
from typing import Any, Dict


class MCPDataLossPreventionGateway:
    IBAN_PATTERN = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{12,30}\b")

    @classmethod
    def inspect_and_filter(cls, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        arg_str = str(arguments)
        if cls.IBAN_PATTERN.search(arg_str) and tool_name not in {"secure_wire_transfer"}:
            return {
                "blocked": True,
                "reason": f"DLP Violation: Unencrypted IBAN detected in arguments for non-clearing tool '{tool_name}'.",
            }
        return {"blocked": False}


gateway = MCPDataLossPreventionGateway()
blocked_call = gateway.inspect_and_filter("web_search", {"query": "Check status for GB29NWBK60161331926819"})
assert blocked_call["blocked"] is True
assert "DLP Violation" in blocked_call["reason"]

allowed_call = gateway.inspect_and_filter("secure_wire_transfer", {"recipient_iban": "GB29NWBK60161331926819"})
assert allowed_call["blocked"] is False
```

## Likely follow-ups

- What false positive risks exist with regex-based DLP filters?
- How do enterprise gateways integrate with commercial DLP solutions (Symantec, Microsoft Purview)?

---

[← Q0697](../../batch_07_mcp_a2a_skills_assistants/0697_preventing_prompt_injection_across_a2a_agent_boundaries/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0699 →](../../batch_07_mcp_a2a_skills_assistants/0699_audit_logging_for_regulatory_compliance/README.md)
