# Q0950 · Auditing agent action intents before tool execution

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Medium |

## Question

Write Python code implementing an immutable action intent auditor that logs structured execution intent records before an agent invokes external banking APIs.

## Answer

Under regulatory scrutiny (OCC, Federal Reserve), every autonomous action taken by an AI agent must have an auditable intent trail: what user prompt prompted the action, what intermediate reasoning led to the tool call, and what exact parameters were submitted.

```python
from datetime import datetime, timezone
from typing import Dict, List, Any


class ActionIntentAuditLogger:
    def __init__(self):
        self.audit_log: List[Dict[str, Any]] = []

    def record_intent(
        self,
        session_id: str,
        user_id: str,
        tool_name: str,
        parameters: Dict[str, Any],
        agent_reasoning: str,
    ) -> str:
        record_id = f"aud_{len(self.audit_log) + 1}"
        entry = {
            "record_id": record_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "user_id": user_id,
            "tool_name": tool_name,
            "parameters": parameters,
            "reasoning": agent_reasoning,
        }
        self.audit_log.append(entry)
        return record_id


auditor = ActionIntentAuditLogger()
rec_id = auditor.record_intent(
    session_id="sess_42",
    user_id="trader_77",
    tool_name="execute_block_trade",
    parameters={"ticker": "JPM", "shares": 5000},
    agent_reasoning="User instructed rebalancing portfolio towards financial sector.",
)

assert rec_id == "aud_1"
assert len(auditor.audit_log) == 1
assert auditor.audit_log[0]["parameters"]["shares"] == 5000
assert "rebalancing" in auditor.audit_log[0]["reasoning"]
```

## Likely follow-ups

- Why must audit logs be stored in Write-Once-Read-Many (WORM) storage compliant with SEC Rule 17a-4?
- How do cryptographic hashes link sequential audit entries to prevent retroactive log tampering?

---

[← Q0949](../../batch_10_ai_security_responsible_ai/0949_agent_tool_call_parameter_schema_validation_with_pydantic_v2/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0951 →](../../batch_10_ai_security_responsible_ai/0951_microsoft_presidio_architecture_analyzers_recognizers_and/README.md)
