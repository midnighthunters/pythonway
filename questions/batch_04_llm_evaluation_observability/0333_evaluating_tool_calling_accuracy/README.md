# Q0333 · Evaluating tool-calling accuracy

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Agent evaluation | Medium |

## Question

Score an agent's tool calls against expected calls: tool selection accuracy, exact argument match, and partial argument credit, with argument normalisation.

## Answer

```python
def _norm(v):
    if isinstance(v, str):
        return " ".join(v.lower().split())
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return v


def score_tool_call(expected: dict, actual: dict | None) -> dict:
    if actual is None or actual.get("name") != expected["name"]:
        return {"tool_correct": False, "args_exact": False, "args_partial": 0.0}
    exp, act = expected.get("args", {}), actual.get("args", {})
    matched = sum(_norm(act.get(k)) == _norm(v) for k, v in exp.items())
    extra = set(act) - set(exp)
    return {"tool_correct": True, "args_exact": matched == len(exp) and not extra,
            "args_partial": matched / len(exp) if exp else 1.0}


def aggregate(pairs: list[tuple[dict, dict | None]]) -> dict:
    scores = [score_tool_call(e, a) for e, a in pairs]
    n = len(scores)
    return {k: sum(s[k] for s in scores) / n for k in ("tool_correct", "args_exact", "args_partial")}


pairs = [
    ({"name": "get_fx_rate", "args": {"pair": "GBPUSD", "date": "2026-09-25"}},
     {"name": "get_fx_rate", "args": {"pair": "gbpusd", "date": "2026-09-25"}}),
    ({"name": "get_balance", "args": {"account_id": "ACC-1", "currency": "GBP"}},
     {"name": "get_balance", "args": {"account_id": "ACC-1", "currency": "USD"}}),
    ({"name": "search_policies", "args": {"query": "travel"}}, {"name": "get_balance", "args": {}}),
]
agg = aggregate(pairs)
assert agg == {"tool_correct": 2 / 3, "args_exact": 1 / 3, "args_partial": 0.5}
```

Normalisation must reflect the tool's own semantics: case-insensitive pair codes are fine here, but not for case-sensitive ids. For free-text arguments such as search queries, exact match is too strict, so use a similarity or judge-based score.

## Likely follow-ups

- How do you score an agent that reaches the right answer with a different but valid sequence of tool calls?

---

[← Q0332](../../batch_04_llm_evaluation_observability/0332_key_point_coverage_metric/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0334 →](../../batch_04_llm_evaluation_observability/0334_agent_trajectory_evaluation/README.md)
