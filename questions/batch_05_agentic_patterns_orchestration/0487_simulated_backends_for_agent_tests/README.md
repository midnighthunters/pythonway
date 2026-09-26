# Q0487 · Simulated backends for agent tests

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Testing | Medium |

## Question

Build a small simulated airline backend (search, hold and confirm, with seat inventory and holds that expire), which agent tests can use deterministically instead of real APIs.

## Answer

```python
class FakeAirline:
    def __init__(self, flights: dict[str, int], clock, hold_ttl: float = 900) -> None:
        self.seats, self.clock, self.ttl = dict(flights), clock, hold_ttl
        self.holds: dict[str, tuple[str, float]] = {}
        self.tickets: list[str] = []
        self._n = 0

    def _expire(self) -> None:
        for hid, (flight, ts) in list(self.holds.items()):
            if self.clock() - ts > self.ttl:
                self.seats[flight] += 1
                del self.holds[hid]

    def search(self) -> dict[str, int]:
        self._expire()
        return {f: s for f, s in self.seats.items() if s > 0}

    def hold(self, flight: str) -> str:
        self._expire()
        if self.seats.get(flight, 0) <= 0:
            raise RuntimeError(f"{flight} sold out")
        self.seats[flight] -= 1
        self._n += 1
        hid = f"H{self._n}"
        self.holds[hid] = (flight, self.clock())
        return hid

    def confirm(self, hold_id: str) -> str:
        self._expire()
        if hold_id not in self.holds:
            raise RuntimeError("hold expired or unknown")
        flight, _ = self.holds.pop(hold_id)
        self.tickets.append(flight)
        return f"TKT-{flight}"


t = [0.0]
api = FakeAirline({"LH903": 1, "BA912": 2}, clock=lambda: t[0])
h = api.hold("LH903")
assert api.search() == {"BA912": 2}
t[0] = 1_000
assert api.search() == {"LH903": 1, "BA912": 2}
try:
    api.confirm(h)
    raise AssertionError
except RuntimeError as e:
    assert "expired" in str(e)
h2 = api.hold("LH903")
assert api.confirm(h2) == "TKT-LH903" and api.tickets == ["LH903"]
```

Simulators let you test the nasty cases (sold out between search and hold, expired holds, partial failures) that are hard to reproduce against real supplier sandboxes. Keep the simulator's behaviour aligned with the real API through contract tests against recorded responses.

## Likely follow-ups

- How do you keep a simulator from drifting away from the real API's behaviour?

---

[← Q0486](../../batch_05_agentic_patterns_orchestration/0486_testing_strategy_for_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0488 →](../../batch_05_agentic_patterns_orchestration/0488_fault_injection_for_agents/README.md)
