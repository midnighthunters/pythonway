# Q0404 · Minimal ReAct loop with a fake model

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent loops | Medium |

## Question

Implement a minimal ReAct-style loop: the model returns either a tool call or a final answer; tool results (or errors) are appended as observations; and the loop stops at a step limit.

## Answer

```python
import json
from typing import Callable


def react(question: str, llm: Callable[[list[dict]], dict], tools: dict[str, Callable], max_steps: int = 5) -> dict:
    messages = [{"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        action = llm(messages)
        if action["type"] == "final":
            return {"answer": action["content"], "steps": step, "messages": messages}
        name, args = action["name"], action.get("args", {})
        tool = tools.get(name)
        if tool is None:
            obs = {"error": f"unknown tool {name!r}; available: {sorted(tools)}"}
        else:
            try:
                obs = {"result": tool(**args)}
            except Exception as e:
                obs = {"error": f"{type(e).__name__}: {e}"}
        messages.append({"role": "assistant", "tool_call": {"name": name, "args": args}})
        messages.append({"role": "tool", "name": name, "content": json.dumps(obs)})
    return {"answer": None, "steps": max_steps, "stopped": "max_steps", "messages": messages}


def get_fx(pair: str) -> float:
    return {"GBPUSD": 1.27}[pair]


script = iter([{"type": "tool", "name": "get_fx", "args": {"pair": "GBPUSD"}},
               {"type": "final", "content": "£100 is about $127."}])
out = react("How many dollars is £100?", lambda m: next(script), {"get_fx": get_fx})
assert out["answer"] == "£100 is about $127." and out["steps"] == 2
assert json.loads(out["messages"][-1]["content"]) == {"result": 1.27}

errors = react("x", lambda m: {"type": "tool", "name": "get_fx", "args": {"pair": "XXX"}}, {"get_fx": get_fx}, 2)
assert errors["stopped"] == "max_steps" and "KeyError" in errors["messages"][-1]["content"]
```

Returning tool errors to the model (instead of raising) lets it recover, for example by retrying with a corrected argument. Real implementations use native tool calling, parallel calls, token budgets and tracing, but the control flow is exactly this.

## Likely follow-ups

- What goes wrong if tool exceptions crash the loop instead of being returned?

---

[← Q0403](../../batch_05_agentic_patterns_orchestration/0403_anatomy_of_an_agent_loop/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0405 →](../../batch_05_agentic_patterns_orchestration/0405_tool_registry_with_schemas_and_permissions/README.md)
