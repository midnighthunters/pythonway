# Q0461 · Blackboard architecture

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Multi-agent | Medium |

## Question

Implement a blackboard system: specialist agents watch a shared fact store, each runs when its preconditions are met and adds new facts, and a controller loops until the goal fact appears or no agent can make progress.

## Answer

```python
from typing import Callable

Agent = tuple[str, Callable[[dict], bool], Callable[[dict], dict]]


def blackboard(facts: dict, agents: list[Agent], goal: str, max_cycles: int = 10) -> dict:
    ran = []
    for _ in range(max_cycles):
        if goal in facts:
            return {"facts": facts, "ran": ran, "status": "goal"}
        progressed = False
        for name, ready, act in agents:
            if ready(facts):
                new = {k: v for k, v in act(facts).items() if k not in facts}
                if new:
                    facts.update(new)
                    ran.append(name)
                    progressed = True
        if not progressed:
            return {"facts": facts, "ran": ran, "status": "stuck"}
    return {"facts": facts, "ran": ran, "status": "max_cycles"}


agents: list[Agent] = [
    ("trade_fetcher", lambda f: "break_id" in f, lambda f: {"trade": {"qty": 1000, "px": 101.20}}),
    ("confirm_fetcher", lambda f: "break_id" in f, lambda f: {"confirm": {"qty": 1000, "px": 101.25}}),
    ("diff_agent", lambda f: "trade" in f and "confirm" in f,
     lambda f: {"diff": {"field": "px", "delta": round(f["confirm"]["px"] - f["trade"]["px"], 4)}}),
    ("resolver", lambda f: "diff" in f, lambda f: {"resolution": f"price mismatch of {f['diff']['delta']}; request amended confirm"}),
]
out = blackboard({"break_id": "BRK-9"}, agents, goal="resolution")
assert out["status"] == "goal" and out["facts"]["resolution"].startswith("price mismatch of 0.05")
assert out["ran"] == ["trade_fetcher", "confirm_fetcher", "diff_agent", "resolver"]
assert blackboard({}, agents, "resolution")["status"] == "stuck"
```

Blackboards suit problems where the order of work isn't known in advance and specialists contribute opportunistically, such as investigations and diagnostics. The shared state is also a natural audit record. A LangGraph state object shared by nodes is a structured blackboard.

## Likely follow-ups

- What problems arise when two agents write conflicting facts?

---

[← Q0460](../../batch_05_agentic_patterns_orchestration/0460_weighted_voting_across_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0462 →](../../batch_05_agentic_patterns_orchestration/0462_agent_communication_options/README.md)
