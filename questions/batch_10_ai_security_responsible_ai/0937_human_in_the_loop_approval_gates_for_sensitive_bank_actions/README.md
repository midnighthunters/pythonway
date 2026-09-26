# Q0937 · Human-in-the-loop approval gates for sensitive bank actions

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Medium |

## Question

Write Python code implementing an asynchronous Human-in-the-Loop (HITL) approval gate for agent workflows, pausing execution until a human manager approves or rejects the action.

## Answer

In banking, autonomous execution of wire transfers, trade orders, or client credit changes without human oversight violates regulatory standards. The agent must pause, persist its execution state, notify an authorized supervisor, and resume only upon receiving cryptographic approval.

```python
import asyncio
from typing import Dict, Optional


class HITLApprovalWorkflow:
    def __init__(self):
        # Maps action_id -> {"status": str, "payload": dict, "future": asyncio.Future}
        self.pending_actions: Dict[str, Dict] = {}

    async def request_approval(self, action_id: str, action_type: str, details: dict) -> bool:
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self.pending_actions[action_id] = {
            "type": action_type,
            "details": details,
            "future": future,
            "status": "PENDING",
        }
        # Pauses agent execution until manager resolves the future
        approved = await future
        return approved

    def resolve_action(self, action_id: str, approved: bool) -> None:
        if action_id in self.pending_actions:
            self.pending_actions[action_id]["status"] = "APPROVED" if approved else "REJECTED"
            self.pending_actions[action_id]["future"].set_result(approved)


async def main():
    hitl = HITLApprovalWorkflow()

    # Agent requests approval for wire transfer
    async def agent_task():
        approved = await hitl.request_approval("act_99", "WIRE_TRANSFER", {"amount": 500_000, "dest": "CHASE_UK"})
        return "PROCEEDED" if approved else "CANCELLED"

    task = asyncio.create_task(agent_task())

    # Check status is pending
    await asyncio.sleep(0.01)
    assert hitl.pending_actions["act_99"]["status"] == "PENDING"

    # Human supervisor approves the action
    hitl.resolve_action("act_99", approved=True)

    result = await task
    assert result == "PROCEEDED"
    assert hitl.pending_actions["act_99"]["status"] == "APPROVED"


asyncio.run(main())
```

## Likely follow-ups

- How does LangGraph's `interrupt()` function implement stateful HITL across durable checkpoints?
- What timeout policies should abort pending actions if no manager responds within 24 hours?

---

[← Q0936](../../batch_10_ai_security_responsible_ai/0936_tool_permission_scopes_and_least_privilege_in_agent_tools/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0938 →](../../batch_10_ai_security_responsible_ai/0938_step_up_authentication_and_totp_verification_in_agent/README.md)
