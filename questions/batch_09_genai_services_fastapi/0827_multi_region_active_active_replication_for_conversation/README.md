# Q0827 · Multi-region active-active replication for conversation state

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Hard |

## Question

Explain how active-active multi-region replication (e.g. AWS DynamoDB Global Tables or Azure Cosmos DB multi-master) handles concurrent user chat writes, and resolve conflict scenarios in Python.

## Answer

In global banking operations (e.g. trading desks in New York, London, and Singapore), users or agents may interact with regional FastAPI instances.

1. **DynamoDB Global Tables**: Use Last-Writer-Wins (LWW) based on NTP-synchronized timestamps. If two writes occur simultaneously in `us-east-1` and `eu-west-1`, the write with the higher timestamp prevails.
2. **Cosmos DB Multi-Region**: Supports custom conflict resolution procedures (stored procedures) or default LWW on `_ts`.
3. **Data Loss Mitigation**: For conversation logs, updates should be modeled as **append-only immutable events** with unique UUIDs rather than mutating a shared state array. This eliminates update collisions entirely.

```python
import uuid
import time
from typing import Dict, List


class DistributedChatEvent:
    def __init__(self, region: str, thread_id: str, role: str, content: str, ts: float):
        self.event_id = str(uuid.uuid4())
        self.region = region
        self.thread_id = thread_id
        self.role = role
        self.content = content
        self.timestamp = ts


def merge_regional_event_streams(streams: List[List[DistributedChatEvent]]) -> List[DistributedChatEvent]:
    '''Merges append-only event streams from multiple active-active cloud regions.'''
    all_events = []
    for stream in streams:
        all_events.extend(stream)
    # Deterministic conflict resolution: sort by timestamp, then event_id
    all_events.sort(key=lambda e: (e.timestamp, e.event_id))
    return all_events


t0 = time.time()
ny_events = [
    DistributedChatEvent("us-east-1", "th_1", "user", "What is EUR LIBOR replacement?", t0),
    DistributedChatEvent("us-east-1", "th_1", "assistant", "ESTR is the euro short-term rate.", t0 + 1.2),
]
ldn_events = [
    DistributedChatEvent("eu-west-1", "th_1", "user", "What about UK SONIA?", t0 + 2.5),
]

merged = merge_regional_event_streams([ny_events, ldn_events])
assert len(merged) == 3
assert merged[0].region == "us-east-1"
assert merged[-1].region == "eu-west-1"
```

## Likely follow-ups

- What is the replication lag between AWS regions in Global Tables, and how does it impact read consistency?
- Why is an event-sourcing design superior to in-place document updates in multi-region NoSQL?

---

[← Q0826](../../batch_09_genai_services_fastapi/0826_conversation_history_pruning_and_summarization_triggers/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0828 →](../../batch_09_genai_services_fastapi/0828_pii_encryption_at_rest_in_nosql_state_stores_with_envelope/README.md)
