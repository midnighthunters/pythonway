# Q0335 · Final-state evaluation for agents

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Agent evaluation | Medium |

## Question

For a rebooking agent, the transcript can look fine while the backend state is wrong. Implement final-state checks: run named predicates over the environment state after the episode and report which failed.

## Answer

```python
from typing import Callable

Check = tuple[str, Callable[[dict], bool]]


def check_final_state(state: dict, checks: list[Check]) -> dict:
    failed = [name for name, pred in checks if not pred(state)]
    return {"pass": not failed, "failed": failed}


checks: list[Check] = [
    ("booking_rebooked", lambda s: s["booking"]["status"] == "rebooked"),
    ("arrives_before_deadline", lambda s: s["booking"]["arrival"] <= s["deadline"]),
    ("no_refund_issued", lambda s: s["refunds"] == []),
    ("user_notified_once", lambda s: len(s["emails"]) == 1),
]
good = {"booking": {"status": "rebooked", "arrival": "2026-10-01T18:00"}, "deadline": "2026-10-01T20:00",
        "refunds": [], "emails": ["confirmation"]}
bad = {**good, "refunds": [{"amount": 250}], "emails": ["confirmation", "confirmation"]}
assert check_final_state(good, checks) == {"pass": True, "failed": []}
assert check_final_state(bad, checks)["failed"] == ["no_refund_issued", "user_notified_once"]
```

The agent runs against a sandboxed environment (fake booking API, in-memory database) that starts from a fixed fixture for each case. Final-state checks are deterministic, cheap and hard to game, which makes them the strongest signal for action-taking agents. Combine them with trajectory checks (was the user asked before rebooking?).

## Likely follow-ups

- How would you build a realistic sandbox for a payments agent?

---

[← Q0334](../../batch_04_llm_evaluation_observability/0334_agent_trajectory_evaluation/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0336 →](../../batch_04_llm_evaluation_observability/0336_report_cost_and_latency_percentiles/README.md)
