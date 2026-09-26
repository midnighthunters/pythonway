# Q0412 · Router pattern

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent patterns | Easy |

## Question

Implement a router that sends a request to a specialist agent based on a classifier's label and confidence, with a generalist fallback for low confidence or unknown labels.

## Answer

```python
from typing import Callable


def route_request(text: str, classify: Callable[[str], tuple[str, float]], agents: dict[str, Callable[[str], str]],
                  fallback: Callable[[str], str], min_conf: float = 0.7) -> tuple[str, str]:
    label, conf = classify(text)
    if conf < min_conf or label not in agents:
        return "generalist", fallback(text)
    return label, agents[label](text)


agents = {"hr": lambda t: "HR agent answer", "it": lambda t: "IT agent answer"}
classify = lambda t: ("it", 0.93) if "vpn" in t.lower() else ("legal", 0.9) if "contract" in t else ("hr", 0.4)
assert route_request("My VPN is down", classify, agents, lambda t: "general") == ("it", "IT agent answer")
assert route_request("Review this contract", classify, agents, lambda t: "general")[0] == "generalist"
assert route_request("Holiday question", classify, agents, lambda t: "general")[0] == "generalist"
```

Routing keeps each specialist's prompt and tool set small and focused, which improves accuracy, cost and permission scoping. The classifier can be a small model, an embedding nearest-neighbour or an LLM with an enum schema. Evaluate routing accuracy on its own, and log the route in every trace.

## Likely follow-ups

- How would you handle a request that needs two specialists?

---

[← Q0411](../../batch_05_agentic_patterns_orchestration/0411_reflection_and_self_correction_for_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0413 →](../../batch_05_agentic_patterns_orchestration/0413_supervisor_multi_agent_pattern/README.md)
