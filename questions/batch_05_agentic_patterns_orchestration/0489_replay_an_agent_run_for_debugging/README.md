# Q0489 · Replay an agent run for debugging

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Debugging | Medium |

## Question

Record an agent run's model responses and tool results, then replay it deterministically against new code, detecting the first point where the new code diverges (a different tool call).

## Answer

```python
class Divergence(Exception):
    pass


class Recorder:
    def __init__(self) -> None:
        self.events: list[dict] = []

    def llm(self, real, messages):
        out = real(messages)
        self.events.append({"kind": "llm", "out": out})
        return out

    def tool(self, real, name, args):
        out = real(name, args)
        self.events.append({"kind": "tool", "name": name, "args": args, "out": out})
        return out


class Replayer:
    def __init__(self, events: list[dict]) -> None:
        self.events, self.i = events, 0

    def _next(self, kind: str) -> dict:
        ev = self.events[self.i]
        self.i += 1
        if ev["kind"] != kind:
            raise Divergence(f"step {self.i}: expected {ev['kind']}, got {kind}")
        return ev

    def llm(self, _real, messages):
        return self._next("llm")["out"]

    def tool(self, _real, name, args):
        ev = self._next("tool")
        if (ev["name"], ev["args"]) != (name, args):
            raise Divergence(f"step {self.i}: recorded {ev['name']}{ev['args']}, new code called {name}{args}")
        return ev["out"]


def agent(io, llm, tool, currency_arg: str = "pair"):
    plan = io.llm(llm, ["convert 100 GBP"])
    rate = io.tool(tool, "get_fx", {currency_arg: plan})
    return io.llm(llm, [f"rate={rate}"])


responses = iter(["GBPUSD", "About $127"])
rec = Recorder()
assert agent(rec, lambda m: next(responses), lambda n, a: 1.27) == "About $127"
assert agent(Replayer(rec.events), None, None) == "About $127"
try:
    agent(Replayer(rec.events), None, None, currency_arg="symbol")
    raise AssertionError
except Divergence as e:
    assert "new code called get_fx{'symbol': 'GBPUSD'}" in str(e)
```

Replays reproduce production bugs locally without calling models or touching real systems, and show exactly where a code change alters behaviour. Scrub sensitive data from recordings, and store them with traces under the same access controls.

## Likely follow-ups

- What makes a divergence expected rather than a bug?

---

[← Q0488](../../batch_05_agentic_patterns_orchestration/0488_fault_injection_for_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0490 →](../../batch_05_agentic_patterns_orchestration/0490_versioning_agents_and_workflows/README.md)
