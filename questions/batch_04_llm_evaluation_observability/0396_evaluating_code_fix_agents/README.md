# Q0396 · Evaluating code-fix agents

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Agent evaluation | Medium |

## Question

Implement SWE-bench-style evaluation for an automated code-fix agent: an issue counts as resolved only if its fail-to-pass tests now pass and its pass-to-pass tests still pass. Report the resolved rate and the regression count.

## Answer

```python
def evaluate_fixes(issues: list[dict], run_tests) -> dict:
    resolved, broke_existing = [], []
    for issue in issues:
        results = run_tests(issue["id"], issue["patch"])
        f2p_ok = all(results[t] for t in issue["fail_to_pass"])
        p2p_ok = all(results[t] for t in issue["pass_to_pass"])
        if f2p_ok and p2p_ok:
            resolved.append(issue["id"])
        if not p2p_ok:
            broke_existing.append(issue["id"])
    return {"resolved_rate": len(resolved) / len(issues), "resolved": resolved, "regressions": broke_existing}


RESULTS = {
    "ISSUE-1": {"test_bug": True, "test_a": True, "test_b": True},
    "ISSUE-2": {"test_bug": True, "test_a": False, "test_b": True},
    "ISSUE-3": {"test_bug": False, "test_a": True, "test_b": True},
}
issues = [{"id": i, "patch": "...", "fail_to_pass": ["test_bug"], "pass_to_pass": ["test_a", "test_b"]}
          for i in RESULTS]
r = evaluate_fixes(issues, lambda issue_id, patch: RESULTS[issue_id])
assert r == {"resolved_rate": 1 / 3, "resolved": ["ISSUE-1"], "regressions": ["ISSUE-2"]}
```

ISSUE-2 "fixed" the bug but broke other behaviour. That is worse than no fix, which is why pass-to-pass tests matter. For production code-fix agents (for example self-patching red CI builds), also track human acceptance of the proposed patches, time to merge, reverts, and the security scan results on patches. Run the patches in isolated sandboxes.

## Likely follow-ups

- Why is "tests pass" insufficient evidence that a patch is correct?

---

[← Q0395](../../batch_04_llm_evaluation_observability/0395_total_cost_including_human_rework/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0397 →](../../batch_04_llm_evaluation_observability/0397_evaluating_an_mcp_tool_server/README.md)
