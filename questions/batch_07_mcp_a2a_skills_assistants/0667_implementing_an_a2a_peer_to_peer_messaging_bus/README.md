# Q0667 · Implementing an A2A Peer-to-Peer messaging bus

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A orchestration | Hard |

## Question

Implement an in-memory Peer-to-Peer messaging bus where autonomous A2A agents can register, broadcast discoveries, and send targeted direct messages to other agents.

## Answer

In decentralized multi-agent systems, agents need to communicate directly without routing through a central supervisor.

```python
from typing import Callable, Dict, List


class A2APeerMessageBus:
    def __init__(self):
        self._subscribers: Dict[str, Callable[[str, str], None]] = {}
        self.message_history: List[Dict[str, str]] = []

    def register_agent(self, agent_id: str, callback: Callable[[str, str], None]):
        self._subscribers[agent_id] = callback

    def send_direct(self, sender_id: str, recipient_id: str, message: str) -> bool:
        if recipient_id not in self._subscribers:
            return False
        self.message_history.append({"from": sender_id, "to": recipient_id, "body": message})
        self._subscribers[recipient_id](sender_id, message)
        return True

    def broadcast(self, sender_id: str, message: str) -> None:
        for aid, callback in self._subscribers.items():
            if aid != sender_id:
                self.message_history.append({"from": sender_id, "to": aid, "body": message})
                callback(sender_id, message)


bus = A2APeerMessageBus()
inbox_b = []
inbox_c = []

bus.register_agent("agent-a", lambda sender, msg: None)
bus.register_agent("agent-b", lambda sender, msg: inbox_b.append((sender, msg)))
bus.register_agent("agent-c", lambda sender, msg: inbox_c.append((sender, msg)))

assert bus.send_direct("agent-a", "agent-b", "Hello B, check counterparty X") is True
assert len(inbox_b) == 1
assert inbox_b[0] == ("agent-a", "Hello B, check counterparty X")

bus.broadcast("agent-a", "Market volatility alert")
assert len(inbox_b) == 2
assert len(inbox_c) == 1
```

## Likely follow-ups

- How can backpressure be handled when an agent's inbox fills up?
- How do you secure peer-to-peer message buses against unauthorized eavesdropping?

---

[← Q0666](../../batch_07_mcp_a2a_skills_assistants/0666_supervisor_worker_topology_using_a2a_protocol/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0668 →](../../batch_07_mcp_a2a_skills_assistants/0668_contract_net_protocol_in_a2a_multi_agent_systems/README.md)
