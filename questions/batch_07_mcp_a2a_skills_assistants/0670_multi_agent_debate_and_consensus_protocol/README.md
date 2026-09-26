# Q0670 · Multi-Agent debate and consensus protocol

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A orchestration | Hard |

## Question

Write Python code for an A2A multi-agent debate protocol where two analyst agents critique each other's conclusions until reaching consensus or reaching a round limit.

## Answer

In high-stakes financial domains (e.g. credit approvals or merger evaluations), single-agent reasoning can suffer from hallucinations or confirmation bias. A debate protocol pits two agents against each other to evaluate evidence.

```python
from typing import Any, Dict, List


class DebateAgent:
    def __init__(self, name: str, stance_bias: float):
        self.name = name
        self.bias = stance_bias

    def formulate_opinion(self, base_val: float, opponent_argument: str) -> float:
        return round((base_val + self.bias) / 2.0, 2)


def run_agent_debate(rounds: int = 3, threshold: float = 0.5) -> Dict[str, Any]:
    agent_a = DebateAgent("BullishAnalyst", 10.0)
    agent_b = DebateAgent("BearishAnalyst", 2.0)

    val_a = 10.0
    val_b = 2.0
    transcript: List[str] = []

    for r in range(rounds):
        diff = abs(val_a - val_b)
        transcript.append(f"Round {r+1}: Agent A={val_a}, Agent B={val_b}, Diff={diff}")
        if diff <= threshold:
            return {"status": "consensus_reached", "final_val": round((val_a + val_b) / 2.0, 2), "transcript": transcript}

        val_a = agent_a.formulate_opinion(val_b, "argument")
        val_b = agent_b.formulate_opinion(val_a, "argument")

    return {"status": "max_rounds_reached", "final_val": round((val_a + val_b) / 2.0, 2), "transcript": transcript}


res = run_agent_debate(rounds=5, threshold=0.5)
assert res["status"] in {"consensus_reached", "max_rounds_reached"}
assert len(res["transcript"]) >= 2
```

## Likely follow-ups

- How does an independent judge agent break a deadlock if debate rounds expire without consensus?
- What are the token cost tradeoffs of multi-agent debate versus single-agent chain-of-thought?

---

[← Q0669](../../batch_07_mcp_a2a_skills_assistants/0669_implementing_a2a_call_for_proposal_and_bidding/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0671 →](../../batch_07_mcp_a2a_skills_assistants/0671_a2a_deadlocks_and_cycle_detection_in_agent_delegation/README.md)
