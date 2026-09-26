# Q0672 · Shared blackboard architecture for A2A collaboration

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A orchestration | Hard |

## Question

Implement an in-memory Shared Blackboard in Python for asynchronous multi-agent coordination with tagged state keys and subscriber notifications.

## Answer

In blackboard systems, autonomous agents do not communicate point-to-point. Instead, they read from and post hypotheses/evidence to a shared blackboard repository.

```python
from typing import Any, Callable, Dict, List


class SharedBlackboard:
    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._listeners: Dict[str, List[Callable[[str, Any], None]]] = {}

    def subscribe(self, key_prefix: str, listener: Callable[[str, Any], None]):
        if key_prefix not in self._listeners:
            self._listeners[key_prefix] = []
        self._listeners[key_prefix].append(listener)

    def write(self, key: str, value: Any) -> None:
        self._state[key] = value
        for prefix, listeners in self._listeners.items():
            if key.startswith(prefix):
                for listener in listeners:
                    listener(key, value)

    def read(self, key: str) -> Any:
        return self._state.get(key)


board = SharedBlackboard()
risk_findings = []
board.subscribe("break:", lambda k, v: risk_findings.append((k, v)))

# Trade reconciliation agent writes a detected break
board.write("break:BRK-001", {"account": "LDN-1", "diff": 500.0})

assert len(risk_findings) == 1
assert risk_findings[0][0] == "break:BRK-001"
assert board.read("break:BRK-001")["diff"] == 500.0
```

## Likely follow-ups

- How does the blackboard pattern decouple agent execution lifecycles?
- How do you prevent race conditions when two agents attempt to update the same key simultaneously?

---

[← Q0671](../../batch_07_mcp_a2a_skills_assistants/0671_a2a_deadlocks_and_cycle_detection_in_agent_delegation/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0673 →](../../batch_07_mcp_a2a_skills_assistants/0673_error_handling_and_failover_in_a2a_worker_pools/README.md)
