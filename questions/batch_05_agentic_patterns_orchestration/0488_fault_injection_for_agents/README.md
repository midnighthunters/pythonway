# Q0488 · Fault injection for agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Testing | Medium |

## Question

Implement a fault-injection wrapper for tools (random timeouts, errors and slow responses with a seeded RNG), and use it to check that an agent's retry logic still completes most tasks.

## Answer

```python
import random
from typing import Callable


def with_faults(fn: Callable, rng: random.Random, p_error: float = 0.2, p_timeout: float = 0.1) -> Callable:
    def wrapped(*args, **kwargs):
        r = rng.random()
        if r < p_timeout:
            raise TimeoutError("injected timeout")
        if r < p_timeout + p_error:
            raise ConnectionError("injected 503")
        return fn(*args, **kwargs)
    return wrapped


def call_with_retries(fn: Callable, attempts: int = 3):
    last = None
    for _ in range(attempts):
        try:
            return fn()
        except (TimeoutError, ConnectionError) as e:
            last = e
    raise last


rng = random.Random(42)
flaky_lookup = with_faults(lambda: "ok", rng)
successes = 0
for _ in range(1_000):
    try:
        call_with_retries(flaky_lookup)
        successes += 1
    except (TimeoutError, ConnectionError):
        pass
assert successes > 950
```

With a 30% per-call fault rate, three attempts give about 97% success (1 - 0.3³). Run the agent end to end under injected faults in CI, and check that failures produce graceful messages and correct compensations, never partial side effects. Chaos tests in staging (dependency outages, slow LLM responses) validate the circuit breakers and timeouts.

## Likely follow-ups

- What should an agent tell the user when a critical tool is down?

---

[← Q0487](../../batch_05_agentic_patterns_orchestration/0487_simulated_backends_for_agent_tests/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0489 →](../../batch_05_agentic_patterns_orchestration/0489_replay_an_agent_run_for_debugging/README.md)
