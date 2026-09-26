# Q0407 · Loop guards: steps, tokens and repetition

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent safety | Medium |

## Question

Implement a guard object that stops an agent when it exceeds a step limit, a token budget, or repeats the same tool call with identical arguments too many times.

## Answer

```python
import json
from collections import Counter


class StopAgent(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class LoopGuard:
    def __init__(self, max_steps: int, max_tokens: int, max_repeats: int = 2) -> None:
        self.max_steps, self.max_tokens, self.max_repeats = max_steps, max_tokens, max_repeats
        self.steps = self.tokens = 0
        self.calls: Counter[str] = Counter()

    def check(self, tokens_used: int, tool_name: str | None = None, args: dict | None = None) -> None:
        self.steps += 1
        self.tokens += tokens_used
        if self.steps > self.max_steps:
            raise StopAgent("max_steps")
        if self.tokens > self.max_tokens:
            raise StopAgent("token_budget")
        if tool_name:
            key = tool_name + json.dumps(args or {}, sort_keys=True)
            self.calls[key] += 1
            if self.calls[key] > self.max_repeats:
                raise StopAgent(f"repeated_call:{tool_name}")


g = LoopGuard(max_steps=10, max_tokens=5_000)
g.check(500, "search", {"q": "policy"})
g.check(500, "search", {"q": "policy"})
try:
    g.check(500, "search", {"q": "policy"})
    raise AssertionError
except StopAgent as e:
    assert e.reason == "repeated_call:search"
g2 = LoopGuard(max_steps=10, max_tokens=1_000)
g2.check(600)
try:
    g2.check(600)
except StopAgent as e:
    assert e.reason == "token_budget"
```

When a guard trips, don't just fail: return a graceful message ("I couldn't complete this; here's what I found so far") with the partial results, log the trace for review, and count guard trips per agent as a quality metric.

## Likely follow-ups

- Why is "same tool with identical arguments" a better repetition signal than "same tool"?

---

[← Q0406](../../batch_05_agentic_patterns_orchestration/0406_format_tool_results_for_the_model/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0408 →](../../batch_05_agentic_patterns_orchestration/0408_detect_cyclic_tool_call_patterns/README.md)
