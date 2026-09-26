# Q0413 · Supervisor multi-agent pattern

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Multi-agent | Medium |

## Question

Implement a supervisor that repeatedly chooses which worker agent acts next (or FINISH) based on the shared history, with a round limit.

## Answer

```python
from typing import Callable


def supervise(task: str, supervisor: Callable[[list[dict]], str], workers: dict[str, Callable[[list[dict]], str]],
              max_rounds: int = 6) -> dict:
    history = [{"from": "user", "content": task}]
    for _ in range(max_rounds):
        choice = supervisor(history)
        if choice == "FINISH":
            return {"status": "done", "history": history}
        if choice not in workers:
            history.append({"from": "system", "content": f"unknown worker {choice!r}"})
            continue
        history.append({"from": choice, "content": workers[choice](history)})
    return {"status": "max_rounds", "history": history}


def supervisor(history: list[dict]) -> str:
    speakers = [h["from"] for h in history]
    if "researcher" not in speakers:
        return "researcher"
    if "writer" not in speakers:
        return "writer"
    return "FINISH"


workers = {"researcher": lambda h: "Found: London cap 180 GBP [pol-7]",
           "writer": lambda h: "Draft: The London hotel cap is 180 GBP [pol-7]."}
out = supervise("Write a note on the London hotel cap", supervisor, workers)
assert out["status"] == "done" and [h["from"] for h in out["history"]] == ["user", "researcher", "writer"]
```

The supervisor centralises control, which makes it easier to reason about, to enforce budgets and to trace. The downsides are an extra LLM call per hop, and a context that grows with every worker's output (so pass summaries, not full transcripts). LangGraph's supervisor pattern implements this with workers as graph nodes or tools.

## Likely follow-ups

- How would you stop the supervisor from bouncing between two workers forever?

---

[← Q0412](../../batch_05_agentic_patterns_orchestration/0412_router_pattern/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0414 →](../../batch_05_agentic_patterns_orchestration/0414_hierarchical_agents/README.md)
