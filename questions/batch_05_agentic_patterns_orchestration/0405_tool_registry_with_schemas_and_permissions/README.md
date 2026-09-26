# Q0405 · Tool registry with schemas and permissions

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Tooling | Medium |

## Question

Build a tool registry: tools are registered with a Pydantic argument model, a side-effect class (read or write) and the roles allowed to use them. It produces tool specs for the model and enforces validation and roles on every call.

## Answer

```python
from dataclasses import dataclass
from typing import Callable, Literal

from pydantic import BaseModel, Field, ValidationError


@dataclass
class Tool:
    name: str
    description: str
    args_model: type[BaseModel]
    fn: Callable
    effect: Literal["read", "write"]
    roles: frozenset[str]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, description: str, args_model: type[BaseModel], effect: str, roles: set[str]):
        def deco(fn):
            self._tools[fn.__name__] = Tool(fn.__name__, description, args_model, fn, effect, frozenset(roles))
            return fn
        return deco

    def specs_for(self, role: str) -> list[dict]:
        return [{"name": t.name, "description": t.description, "parameters": t.args_model.model_json_schema()}
                for t in self._tools.values() if role in t.roles]

    def call(self, name: str, args: dict, role: str) -> dict:
        tool = self._tools.get(name)
        if tool is None or role not in tool.roles:
            return {"ok": False, "error": f"tool {name!r} not available for role {role!r}"}
        try:
            parsed = tool.args_model.model_validate(args)
        except ValidationError as e:
            return {"ok": False, "error": e.errors()[0]["msg"]}
        return {"ok": True, "result": tool.fn(**parsed.model_dump()), "effect": tool.effect}


reg = ToolRegistry()


class BalanceArgs(BaseModel):
    account_id: str = Field(pattern=r"^ACC-\d{4}$")


@reg.register("Get the balance of an account", BalanceArgs, "read", {"analyst", "ops"})
def get_balance(account_id: str) -> str:
    return f"{account_id}: 1,000.00 GBP"


assert [s["name"] for s in reg.specs_for("analyst")] == ["get_balance"] and reg.specs_for("guest") == []
assert reg.call("get_balance", {"account_id": "ACC-0001"}, "ops")["ok"]
assert not reg.call("get_balance", {"account_id": "x"}, "ops")["ok"]
assert "not available" in reg.call("get_balance", {"account_id": "ACC-0001"}, "guest")["error"]
```

The model only sees the tools its role allows (smaller context, fewer mistakes). Every call is still re-checked, because the model can hallucinate tool names or be manipulated into calling tools it shouldn't.

## Likely follow-ups

- Where would per-record authorisation (can this user see ACC-0001?) live?

---

[← Q0404](../../batch_05_agentic_patterns_orchestration/0404_minimal_react_loop_with_a_fake_model/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0406 →](../../batch_05_agentic_patterns_orchestration/0406_format_tool_results_for_the_model/README.md)
