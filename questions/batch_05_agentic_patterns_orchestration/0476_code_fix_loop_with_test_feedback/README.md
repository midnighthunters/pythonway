# Q0476 · Code-fix loop with test feedback

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent loops | Medium |

## Question

Implement a bounded fix loop: run the tests, give the failures to a patch proposer, apply its patch, and repeat until the tests pass, the iteration cap is hit, or the same failures repeat (no progress).

## Answer

```python
from typing import Callable


def fix_loop(code: dict[str, str], run_tests: Callable[[dict], set[str]],
             propose: Callable[[dict, set[str]], dict[str, str]], max_iters: int = 4) -> dict:
    seen: list[frozenset[str]] = []
    for i in range(max_iters + 1):
        failures = run_tests(code)
        if not failures:
            return {"status": "fixed", "iterations": i, "code": code}
        if frozenset(failures) in seen:
            return {"status": "no_progress", "iterations": i, "failures": sorted(failures)}
        seen.append(frozenset(failures))
        if i == max_iters:
            break
        code = {**code, **propose(code, failures)}
    return {"status": "gave_up", "iterations": max_iters, "failures": sorted(failures)}


def run_tests(code: dict[str, str]) -> set[str]:
    env: dict = {}
    exec(code["fees.py"], env)
    failures = set()
    if env["fee"](100) != 1.0:
        failures.add("test_fee_basic")
    if env["fee"](0) != 0:
        failures.add("test_fee_zero")
    return failures


def propose(code: dict[str, str], failures: set[str]) -> dict[str, str]:
    if "test_fee_basic" in failures:
        return {"fees.py": "def fee(x):\n    return x * 0.01 if x else 1"}
    return {"fees.py": "def fee(x):\n    return x * 0.01"}


out = fix_loop({"fees.py": "def fee(x):\n    return x * 0.1"}, run_tests, propose)
assert out["status"] == "fixed" and out["iterations"] == 2
stuck = fix_loop({"fees.py": "def fee(x):\n    return 7"}, run_tests, lambda c, f: {"fees.py": "def fee(x):\n    return 7"})
assert stuck["status"] == "no_progress"
```

The first patch fixed one test and broke nothing, and the second fixed the rest. `exec` stands in here for running tests in a sandboxed container, which is what production must do. The no-progress check saves money when the agent keeps making the same mistake.

## Likely follow-ups

- How would you stop the agent from "fixing" tests by weakening the assertions?

---

[← Q0475](../../batch_05_agentic_patterns_orchestration/0475_agentic_code_fix_loop_design/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0477 →](../../batch_05_agentic_patterns_orchestration/0477_fraud_investigation_agent_design/README.md)
