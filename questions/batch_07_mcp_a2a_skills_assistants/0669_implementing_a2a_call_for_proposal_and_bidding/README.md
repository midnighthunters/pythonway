# Q0669 · Implementing A2A Call for Proposal and Bidding

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A orchestration | Hard |

## Question

Write Python code implementing the Contract Net Protocol (CFP, Bidding, Award, Result) between a Manager agent and two Bidder agents.

## Answer

```python
from typing import Any, Dict, List, Optional


class ContractorAgent:
    def __init__(self, name: str, cost_per_unit: float, capacity: int):
        self.name = name
        self.cost_per_unit = cost_per_unit
        self.capacity = capacity

    def evaluate_cfp(self, task_spec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        units = task_spec.get("units", 1)
        if units > self.capacity:
            return None
        total_cost = units * self.cost_per_unit
        return {"bidder": self.name, "cost": total_cost}

    def execute_awarded_task(self, task_spec: Dict[str, Any]) -> str:
        return f"{self.name} completed {task_spec['units']} units successfully."


class ManagerAgent:
    def __init__(self, contractors: List[ContractorAgent]):
        self.contractors = contractors

    def run_auction(self, task_spec: Dict[str, Any]) -> Dict[str, Any]:
        bids = []
        for c in self.contractors:
            bid = c.evaluate_cfp(task_spec)
            if bid is not None:
                bids.append((bid["cost"], c, bid))

        if not bids:
            return {"status": "failed", "reason": "No bids received"}

        bids.sort(key=lambda x: x[0])
        winning_cost, winning_contractor, win_bid = bids[0]

        result = winning_contractor.execute_awarded_task(task_spec)
        return {
            "status": "awarded",
            "winner": win_bid["bidder"],
            "winning_cost": winning_cost,
            "result": result,
        }


c1 = ContractorAgent("HighSpeedGPUWorker", cost_per_unit=2.0, capacity=100)
c2 = ContractorAgent("BudgetCPUWorker", cost_per_unit=0.5, capacity=20)

mgr = ManagerAgent([c1, c2])

# Task with 10 units: c2 is cheaper and has capacity
res1 = mgr.run_auction({"units": 10})
assert res1["winner"] == "BudgetCPUWorker"
assert res1["winning_cost"] == 5.0

# Task with 50 units: c2 exceeds capacity, so c1 wins
res2 = mgr.run_auction({"units": 50})
assert res2["winner"] == "HighSpeedGPUWorker"
assert res2["winning_cost"] == 100.0
```

## Likely follow-ups

- How do you prevent contractors from colluding or gaming bids in an open A2A market?
- How should timeouts during the bidding window be managed?

---

[← Q0668](../../batch_07_mcp_a2a_skills_assistants/0668_contract_net_protocol_in_a2a_multi_agent_systems/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0670 →](../../batch_07_mcp_a2a_skills_assistants/0670_multi_agent_debate_and_consensus_protocol/README.md)
