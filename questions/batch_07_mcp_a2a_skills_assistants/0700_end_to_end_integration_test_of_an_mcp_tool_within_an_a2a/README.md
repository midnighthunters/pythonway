# Q0700 · End-to-end integration test of an MCP tool within an A2A agent

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP and A2A security | Hard |

## Question

Write an end-to-end integration test in Python demonstrating an A2A agent that dynamically queries an internal MCP server tool to resolve an inquiry and returns a completed task.

## Answer

```python
import json
from typing import Any, Dict


class MockMCPServer:
    def handle_tool_call(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if name == "get_account_balance":
            return {"content": [{"type": "text", "text": "Balance: $1,250,000.00"}], "isError": False}
        return {"content": [{"type": "text", "text": "Tool not found"}], "isError": True}


class AccountServiceA2AAgent:
    def __init__(self, mcp_server: MockMCPServer):
        self.mcp_server = mcp_server

    def handle_a2a_task(self, task_payload: Dict[str, Any]) -> Dict[str, Any]:
        task_id = task_payload["task_id"]
        skill_id = task_payload["skill_id"]
        acc_id = task_payload["input"][0]["data"]["account_id"]

        if skill_id != "inquire_balance":
            return {"task_id": task_id, "status": "failed", "error": "Unknown skill"}

        mcp_res = self.mcp_server.handle_tool_call("get_account_balance", {"account_id": acc_id})
        tool_output = mcp_res["content"][0]["text"]

        return {
            "task_id": task_id,
            "status": "completed",
            "output": [
                {"type": "text", "text": f"Successfully retrieved balance for {acc_id}: {tool_output}"},
                {"type": "data", "data": {"account_id": acc_id, "balance_usd": 1250000.0}},
            ],
        }


mcp_srv = MockMCPServer()
a2a_agent = AccountServiceA2AAgent(mcp_srv)

task_request = {
    "task_id": "tsk-integ-001",
    "skill_id": "inquire_balance",
    "input": [{"type": "data", "data": {"account_id": "ACCT-90210"}}],
}

response = a2a_agent.handle_a2a_task(task_request)
assert response["status"] == "completed"
assert "Balance: $1,250,000.00" in response["output"][0]["text"]
assert response["output"][1]["data"]["balance_usd"] == 1250000.0
```

## Likely follow-ups

- How would you mock network latency and transport failures in this test?
- How do contract tests (e.g. Pact) prevent schema drift between MCP and A2A endpoints?

---

[← Q0699](../../batch_07_mcp_a2a_skills_assistants/0699_audit_logging_for_regulatory_compliance/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md)
