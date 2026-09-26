# Q0451 · Perceive, act, verify loop

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent types | Medium |

## Question

Implement a perceive-act-verify loop for a GUI-style agent: act, re-perceive, and check the expected change happened, retrying a bounded number of times before failing clearly.

## Answer

```python
from typing import Callable


def act_and_verify(perceive: Callable[[], dict], act: Callable[[dict], None], action: dict,
                   expect: Callable[[dict, dict], bool], retries: int = 2) -> dict:
    for attempt in range(1, retries + 2):
        before = perceive()
        act(action)
        after = perceive()
        if expect(before, after):
            return {"ok": True, "attempts": attempt}
    return {"ok": False, "attempts": retries + 1, "last_screen": after}


screen = {"page": "form", "fields": {}, "submitted": False}
flaky = {"misses": 1}


def perceive() -> dict:
    return {"page": screen["page"], "fields": dict(screen["fields"]), "submitted": screen["submitted"]}


def act(a: dict) -> None:
    if a["type"] == "type":
        if flaky["misses"]:
            flaky["misses"] -= 1
            return
        screen["fields"][a["field"]] = a["text"]


res = act_and_verify(perceive, act, {"type": "type", "field": "amount", "text": "250.00"},
                     lambda b, a: a["fields"].get("amount") == "250.00")
assert res == {"ok": True, "attempts": 2}
never = act_and_verify(perceive, lambda a: None, {"type": "click", "target": "submit"},
                       lambda b, a: a["submitted"], retries=1)
assert not never["ok"] and never["attempts"] == 2
```

The first keystroke "missed" (as happens with real UIs), and verification caught it. Without verification, agents report success for actions that never happened. The same verify-after-act discipline applies to API agents: re-read the booking after rebooking.

## Likely follow-ups

- How would you verify an action whose effect only appears asynchronously?

---

[← Q0450](../../batch_05_agentic_patterns_orchestration/0450_computer_use_and_browser_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0452 →](../../batch_05_agentic_patterns_orchestration/0452_queue_triggered_agents/README.md)
