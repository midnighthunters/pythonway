# Q0690 · Calendar and meeting management via personal assistant

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Personal AI assistants | Medium |

## Question

Write Python code for an assistant tool that checks calendar availability across multiple meeting attendees and finds the earliest open mutual slot.

## Answer

```python
from typing import List, Optional, Tuple


def find_earliest_mutual_slot(
    attendee_schedules: List[List[Tuple[int, int]]], work_start: int = 9, work_end: int = 17, duration: int = 1
) -> Optional[int]:
    busy_hours = set()
    for schedule in attendee_schedules:
        for start, end in schedule:
            for h in range(start, end):
                busy_hours.add(h)

    for candidate in range(work_start, work_end - duration + 1):
        if all((candidate + d) not in busy_hours for d in range(duration)):
            return candidate
    return None


schedules = [[(9, 10), (13, 14)], [(10, 12)]]
slot = find_earliest_mutual_slot(schedules, work_start=9, work_end=17, duration=1)
assert slot == 12
```

## Likely follow-ups

- How do you handle timezone differences across global bank hubs (London, New York, Singapore)?
- How should the assistant handle tentative vs confirmed calendar bookings?

---

[← Q0689](../../batch_07_mcp_a2a_skills_assistants/0689_intent_routing_between_local_tools_and_specialized_a2a/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0691 →](../../batch_07_mcp_a2a_skills_assistants/0691_proactive_vs_reactive_assistant_behavior_triggers_and/README.md)
