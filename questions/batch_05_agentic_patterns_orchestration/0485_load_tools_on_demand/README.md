# Q0485 · Load tools on demand

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Tooling | Medium |

## Question

Implement dynamic tool loading: the agent starts with a small active tool set plus a `find_tools(query)` meta-tool that searches the catalogue and activates matches, and the dispatcher only allows active tools.

## Answer

```python
import re


class DynamicTools:
    def __init__(self, catalogue: dict[str, str], initial: set[str], max_active: int = 6) -> None:
        self.catalogue, self.active, self.max_active = catalogue, set(initial), max_active

    def find_tools(self, query: str, k: int = 2) -> list[str]:
        q = set(re.findall(r"[a-z]+", query.lower()))
        scored = sorted(((len(q & set(re.findall(r"[a-z]+", desc.lower()))), name)
                         for name, desc in self.catalogue.items() if name not in self.active), reverse=True)
        found = [name for score, name in scored[:k] if score > 0]
        room = self.max_active - len(self.active)
        self.active.update(found[:max(0, room)])
        return found[:max(0, room)]

    def dispatch(self, name: str) -> str:
        if name not in self.active:
            raise PermissionError(f"{name} is not loaded; call find_tools first")
        return f"called {name}"


catalogue = {"search_policies": "search HR and travel policies", "get_fx_rate": "currency exchange rate lookup",
             "book_room": "book a meeting room", "get_payslip": "employee payslip and salary details"}
dt = DynamicTools(catalogue, initial={"search_policies"})
try:
    dt.dispatch("get_fx_rate")
    raise AssertionError
except PermissionError:
    pass
assert dt.find_tools("what is the exchange rate for currency GBP") == ["get_fx_rate"]
assert dt.dispatch("get_fx_rate") == "called get_fx_rate"
```

Activation should still respect permissions: `find_tools` must only search the tools this user and assistant are allowed to have, otherwise it becomes a privilege-escalation path. Adding tools mid-run changes the prompt, which costs prompt-cache hits, so batch the loading where possible.

## Likely follow-ups

- How would you stop `find_tools` from exposing tools the user isn't entitled to?

---

[← Q0484](../../batch_05_agentic_patterns_orchestration/0484_tool_selection_at_scale/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0486 →](../../batch_05_agentic_patterns_orchestration/0486_testing_strategy_for_agents/README.md)
