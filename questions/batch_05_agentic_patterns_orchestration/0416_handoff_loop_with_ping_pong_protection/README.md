# Q0416 · Handoff loop with ping-pong protection

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Multi-agent | Medium |

## Question

Implement a swarm-style loop where the active agent either replies or hands off to another agent, and the loop prevents infinite handoff ping-pong.

## Answer

```python
from typing import Callable


def run_swarm(message: str, agents: dict[str, Callable[[str], dict]], start: str, max_handoffs: int = 3) -> dict:
    active, path = start, [start]
    for _ in range(max_handoffs + 1):
        out = agents[active](message)
        if "handoff" not in out:
            return {"agent": active, "reply": out["reply"], "path": path}
        target = out["handoff"]
        if target not in agents or target in path[-2:-1]:
            return {"agent": active, "reply": "Let me connect you with a person who can help.", "path": path,
                    "escalated": True}
        active = target
        path.append(target)
    return {"agent": active, "reply": "Let me connect you with a person who can help.", "path": path, "escalated": True}


agents = {
    "triage": lambda m: {"handoff": "billing"} if "invoice" in m else {"reply": "How can I help?"},
    "billing": lambda m: {"reply": "Your invoice was sent on 1 Oct."} if "copy" in m else {"handoff": "triage"},
}
assert run_swarm("I need a copy of my invoice", agents, "triage") == {
    "agent": "billing", "reply": "Your invoice was sent on 1 Oct.", "path": ["triage", "billing"]}
bounced = run_swarm("invoice dispute", agents, "triage")
assert bounced["escalated"] and bounced["path"] == ["triage", "billing"]
```

Handing straight back to the agent you just came from is treated as ping-pong, and the conversation escalates to a human instead of looping. The handoff should also carry a structured summary, so the receiving agent doesn't re-ask the user everything.

## Likely follow-ups

- What should the handoff payload contain so the user isn't asked to repeat themselves?

---

[← Q0415](../../batch_05_agentic_patterns_orchestration/0415_handoffs_versus_agents_as_tools/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0417 →](../../batch_05_agentic_patterns_orchestration/0417_parallel_tool_execution_with_timeouts/README.md)
