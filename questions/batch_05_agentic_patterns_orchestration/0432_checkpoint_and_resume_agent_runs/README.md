# Q0432 · Checkpoint and resume agent runs

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Durability | Medium |

## Question

Implement step-level checkpointing: persist the state after each step, and on restart resume from the last checkpoint without re-running completed side-effecting steps.

## Answer

```python
import json
from typing import Callable


class CheckpointStore:
    def __init__(self) -> None:
        self.data: dict[str, str] = {}

    def save(self, run_id: str, state: dict) -> None:
        self.data[run_id] = json.dumps(state)

    def load(self, run_id: str) -> dict | None:
        raw = self.data.get(run_id)
        return json.loads(raw) if raw else None


def run_steps(run_id: str, steps: list[tuple[str, Callable[[dict], dict]]], store: CheckpointStore) -> dict:
    state = store.load(run_id) or {"completed": [], "vars": {}}
    for name, fn in steps:
        if name in state["completed"]:
            continue
        state["vars"].update(fn(state["vars"]))
        state["completed"].append(name)
        store.save(run_id, state)
    return state


emails: list[str] = []
crash = {"armed": True}


def send_email(v: dict) -> dict:
    emails.append(v["draft"])
    return {"sent": True}


def slow_step(v: dict) -> dict:
    if crash["armed"]:
        crash["armed"] = False
        raise RuntimeError("pod evicted")
    return {"archived": True}


steps = [("draft", lambda v: {"draft": "Hello"}), ("send", send_email), ("archive", slow_step)]
store = CheckpointStore()
try:
    run_steps("run-1", steps, store)
except RuntimeError:
    pass
final = run_steps("run-1", steps, store)
assert final["completed"] == ["draft", "send", "archive"] and emails == ["Hello"]
```

The email is sent exactly once even though the run crashed and restarted. The gap is a crash between executing a side effect and saving the checkpoint, which would re-send. Close it with idempotency keys on the side effect, or an outbox. LangGraph checkpointers (in-memory, SQLite, Postgres) provide the checkpoint-per-step part out of the box.

## Likely follow-ups

- Where exactly is the remaining duplicate-send window, and how do you close it?

---

[← Q0431](../../batch_05_agentic_patterns_orchestration/0431_designing_agent_state/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0433 →](../../batch_05_agentic_patterns_orchestration/0433_durable_execution_for_long_running_agents/README.md)
