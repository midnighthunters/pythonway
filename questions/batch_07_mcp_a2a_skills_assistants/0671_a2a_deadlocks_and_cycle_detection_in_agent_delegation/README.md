# Q0671 · A2A deadlocks and cycle detection in agent delegation

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A orchestration | Hard |

## Question

Write Python code that detects cycles in A2A task delegation graphs (e.g. Agent A delegates to B, B to C, C back to A).

## Answer

Unconstrained agentic delegation can cause recursive deadlocks where agents delegate tasks back to previous callers, consuming resources and freezing runs.

```python
from typing import Dict, List, Set


class DelegationCycleDetector:
    def __init__(self):
        self._graph: Dict[str, List[str]] = {}

    def add_delegation(self, from_agent: str, to_agent: str) -> None:
        if from_agent not in self._graph:
            self._graph[from_agent] = []
        self._graph[from_agent].append(to_agent)

    def has_cycle(self) -> bool:
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def _dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self._graph.get(node, []):
                if neighbor not in visited:
                    if _dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in list(self._graph.keys()):
            if node not in visited:
                if _dfs(node):
                    return True
        return False


detector = DelegationCycleDetector()
detector.add_delegation("AgentA", "AgentB")
detector.add_delegation("AgentB", "AgentC")
assert detector.has_cycle() is False

# Introducing cycle
detector.add_delegation("AgentC", "AgentA")
assert detector.has_cycle() is True
```

## Likely follow-ups

- How can passing a visited agent set inside the A2A `context` block prevent cycles at runtime?
- What should the calling agent do if an A2A delegation returns a `409 Cycle Detected` error?

---

[← Q0670](../../batch_07_mcp_a2a_skills_assistants/0670_multi_agent_debate_and_consensus_protocol/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0672 →](../../batch_07_mcp_a2a_skills_assistants/0672_shared_blackboard_architecture_for_a2a_collaboration/README.md)
