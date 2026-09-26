# Q0481 · Per-user rate limits on agent tools

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent safety | Medium |

## Question

Limit how often an agent can call a sensitive tool on behalf of each user (for example at most 5 emails per 10 minutes), using a sliding window with an injectable clock.

## Answer

```python
from collections import defaultdict, deque


class SlidingWindowLimiter:
    def __init__(self, limit: int, window_s: float, clock) -> None:
        self.limit, self.window, self.clock = limit, window_s, clock
        self.events: dict[tuple[str, str], deque[float]] = defaultdict(deque)

    def allow(self, user: str, tool: str) -> bool:
        now = self.clock()
        q = self.events[(user, tool)]
        while q and q[0] <= now - self.window:
            q.popleft()
        if len(q) >= self.limit:
            return False
        q.append(now)
        return True


t = [0.0]
lim = SlidingWindowLimiter(limit=5, window_s=600, clock=lambda: t[0])
results = []
for i in range(7):
    t[0] = i * 10
    results.append(lim.allow("u-priya", "send_email"))
assert results == [True] * 5 + [False, False]
assert lim.allow("u-tom", "send_email")
t[0] = 601
assert lim.allow("u-priya", "send_email")
```

Rate limits contain the blast radius of a compromised or looping agent (a prompt-injected assistant can't mass-mail the address book). Make limit hits visible: tell the agent it is rate-limited, alert on unusual patterns, and use a shared store (Redis) across replicas.

## Likely follow-ups

- Should limits be per agent, per user, or both?

---

[← Q0480](../../batch_05_agentic_patterns_orchestration/0480_policy_engine_for_tool_calls/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0482 →](../../batch_05_agentic_patterns_orchestration/0482_detect_goal_drift_during_a_run/README.md)
