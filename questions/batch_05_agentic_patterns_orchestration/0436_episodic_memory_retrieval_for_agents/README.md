# Q0436 · Episodic memory retrieval for agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Memory | Medium |

## Question

Implement episodic memory: store past task episodes (the task, the outcome and a lesson learned) per user, and retrieve lessons from the most similar successful episodes to include as hints for a new task.

## Answer

```python
import math
import re
from collections import Counter

STOP = {"the", "a", "for", "to", "of", "and", "my", "in", "on"}


def vec(text: str) -> Counter:
    return Counter(w for w in re.findall(r"[a-z]+", text.lower()) if w not in STOP)


def cos(a: Counter, b: Counter) -> float:
    d = sum(a[k] * b[k] for k in a)
    na, nb = math.sqrt(sum(v * v for v in a.values())), math.sqrt(sum(v * v for v in b.values()))
    return d / (na * nb) if na and nb else 0.0


class EpisodicMemory:
    def __init__(self) -> None:
        self.episodes: list[dict] = []

    def add(self, user: str, task: str, success: bool, lesson: str) -> None:
        self.episodes.append({"user": user, "task": task, "success": success, "lesson": lesson})

    def hints(self, user: str, task: str, k: int = 2, min_sim: float = 0.3) -> list[str]:
        q = vec(task)
        scored = [(cos(q, vec(e["task"])), e["lesson"]) for e in self.episodes if e["user"] == user and e["success"]]
        return [lesson for s, lesson in sorted(scored, reverse=True)[:k] if s >= min_sim]


mem = EpisodicMemory()
mem.add("priya", "rebook cancelled flight to Frankfurt", True, "Check fare class before rebooking; basic fares block changes.")
mem.add("priya", "file quarterly expense report", True, "Attach receipts as PDF; the portal rejects images.")
mem.add("tom", "rebook cancelled flight to Paris", True, "Tom prefers morning flights.")
assert mem.hints("priya", "rebook my cancelled flight to Zurich") == [
    "Check fare class before rebooking; basic fares block changes."]
assert mem.hints("priya", "book a meeting room") == []
```

Other users' episodes are never retrieved. Use real embeddings in production, keep lessons short and reviewed (a bad lesson repeats forever), and let lessons expire when systems change.

## Likely follow-ups

- How would you stop a wrong "lesson" from spreading across many future runs?

---

[← Q0435](../../batch_05_agentic_patterns_orchestration/0435_short_term_versus_long_term_agent_memory/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0437 →](../../batch_05_agentic_patterns_orchestration/0437_scratchpads_and_working_notes/README.md)
