# Q0666 · Supervisor-Worker topology using A2A protocol

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A orchestration | Hard |

## Question

Implement a Supervisor-Worker agentic pattern in Python using the A2A protocol, where a Supervisor agent decomposes a request into sub-tasks and delegates to two specialized worker agents.

## Answer

```python
from typing import Any, Dict, List


class MockA2AWorkerAgent:
    def __init__(self, agent_name: str, specialty: str):
        self.agent_name = agent_name
        self.specialty = specialty

    def execute_task(self, task_input: str) -> Dict[str, Any]:
        return {
            "agent": self.agent_name,
            "status": "completed",
            "result": f"{self.specialty} processed: '{task_input}'",
        }


class A2ASupervisor:
    def __init__(self, workers: Dict[str, MockA2AWorkerAgent]):
        self.workers = workers

    def orchestrate(self, user_goal: str) -> Dict[str, Any]:
        results = {}
        if "risk" in user_goal.lower():
            results["risk"] = self.workers["risk_agent"].execute_task("Analyze market exposure")
        if "compliance" in user_goal.lower():
            results["compliance"] = self.workers["compliance_agent"].execute_task("Check sanction lists")

        summary = "Supervisor plan executed: " + "; ".join(r["result"] for r in results.values())
        return {"goal": user_goal, "delegations": results, "final_summary": summary}


workers = {
    "risk_agent": MockA2AWorkerAgent("RiskAgent", "VaR and Stress Test"),
    "compliance_agent": MockA2AWorkerAgent("ComplianceAgent", "AML and Sanctions"),
}

supervisor = A2ASupervisor(workers)
res = supervisor.orchestrate("Conduct comprehensive risk and compliance assessment for trade TX-10")

assert "RiskAgent" in res["delegations"]["risk"]["agent"]
assert "ComplianceAgent" in res["delegations"]["compliance"]["agent"]
assert "Supervisor plan executed" in res["final_summary"]
```

## Likely follow-ups

- How does the supervisor handle one worker failing while the other succeeds?
- When should worker tasks be dispatched in parallel versus sequentially?

---

[← Q0665](../../batch_07_mcp_a2a_skills_assistants/0665_building_an_in_memory_a2a_task_engine/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0667 →](../../batch_07_mcp_a2a_skills_assistants/0667_implementing_an_a2a_peer_to_peer_messaging_bus/README.md)
