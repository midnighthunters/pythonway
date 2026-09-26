# Q0465 · Stream agent progress events

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | UX engineering | Medium |

## Question

Implement an agent runner that yields typed progress events (status, tool start and end, token deltas, final answer), so the UI can show what the agent is doing instead of a spinner.

## Answer

```python
from typing import Iterator


def run_agent_stream(question: str, plan: list[tuple[str, str]], answer_tokens: list[str]) -> Iterator[dict]:
    yield {"type": "status", "text": "Planning"}
    results = []
    for tool, arg in plan:
        yield {"type": "tool_start", "tool": tool, "summary": f"{tool}({arg})"}
        results.append(f"{tool}:{arg}:ok")
        yield {"type": "tool_end", "tool": tool, "ok": True}
    yield {"type": "status", "text": "Writing answer"}
    for tok in answer_tokens:
        yield {"type": "token", "text": tok}
    yield {"type": "final", "answer": "".join(answer_tokens), "tool_results": len(results)}


events = list(run_agent_stream("rebook", [("search_flights", "FRA"), ("hold_seat", "LH903")],
                               ["You're ", "on ", "LH903."]))
kinds = [e["type"] for e in events]
assert kinds == ["status", "tool_start", "tool_end", "tool_start", "tool_end", "status", "token", "token", "token", "final"]
assert events[-1]["answer"] == "You're on LH903."
```

Send these over SSE or WebSocket with an event name per type. Don't stream raw tool arguments or outputs that may contain sensitive data, only user-safe summaries. End with a terminal event, so clients can tell completion from a dropped connection. LangGraph's streaming modes (`updates`, `messages`, `custom`) map directly onto this.

## Likely follow-ups

- Which events would you hide from end users but keep in traces?

---

[← Q0464](../../batch_05_agentic_patterns_orchestration/0464_stateless_versus_stateful_agent_services/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0466 →](../../batch_05_agentic_patterns_orchestration/0466_pause_and_resume_an_agent_with_generators/README.md)
