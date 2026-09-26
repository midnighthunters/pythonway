# Q0409 · Plan-and-execute agent

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Planning patterns | Medium |

## Question

Implement plan-and-execute: a planner produces the steps (tool plus arguments, where arguments may reference earlier results as `$1`, `$2`), an executor runs them in order, and a final step synthesises the answer.

## Answer

```python
import re
from typing import Callable


def resolve(value, results: list):
    if isinstance(value, str):
        m = re.fullmatch(r"\$(\d+)", value)
        if m:
            return results[int(m.group(1)) - 1]
        return re.sub(r"\$(\d+)", lambda mm: str(results[int(mm.group(1)) - 1]), value)
    return value


def plan_and_execute(task: str, planner: Callable[[str], list[dict]], tools: dict[str, Callable],
                     synthesize: Callable[[str, list], str]) -> dict:
    plan = planner(task)
    results = []
    for i, step in enumerate(plan, 1):
        args = {k: resolve(v, results) for k, v in step["args"].items()}
        results.append(tools[step["tool"]](**args))
    return {"plan": plan, "results": results, "answer": synthesize(task, results)}


tools = {"lookup_employee": lambda name: {"Priya": "E-17"}[name],
         "get_leave_balance": lambda employee_id: {"E-17": 12}[employee_id],
         "calc": lambda expr: eval(expr, {"__builtins__": {}}, {})}
planner = lambda task: [{"tool": "lookup_employee", "args": {"name": "Priya"}},
                        {"tool": "get_leave_balance", "args": {"employee_id": "$1"}},
                        {"tool": "calc", "args": {"expr": "$2 - 3"}}]
out = plan_and_execute("How many leave days will Priya have after a 3-day trip?", planner, tools,
                       lambda t, r: f"Priya will have {r[-1]} days left.")
assert out["results"] == ["E-17", 12, 9] and out["answer"] == "Priya will have 9 days left."
```

Plan-and-execute uses fewer LLM calls than ReAct (one plan, then cheap execution), shows the plan upfront (good for approvals), and parallelises independent steps. The weakness is brittleness when a step's result invalidates the plan, which is what re-planning fixes. Note: the `calc` tool uses a restricted `eval` only for the demo. Never eval model-provided expressions in production; use a safe expression parser.

## Likely follow-ups

- How would you let a human approve the plan before execution?

---

[← Q0408](../../batch_05_agentic_patterns_orchestration/0408_detect_cyclic_tool_call_patterns/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0410 →](../../batch_05_agentic_patterns_orchestration/0410_re_planning_after_a_failed_step/README.md)
