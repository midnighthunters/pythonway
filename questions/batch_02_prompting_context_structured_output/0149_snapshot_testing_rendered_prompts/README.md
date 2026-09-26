# Q0149 · Snapshot testing rendered prompts

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt testing | Medium |

## Question

Implement snapshot testing for prompts: render each template with fixed fixtures, compare with stored snapshots, and show a readable diff on mismatch, so every prompt change is visible in code review.

## Answer

```python
import difflib


def check_snapshot(name: str, rendered: str, snapshots: dict[str, str], update: bool = False) -> str | None:
    old = snapshots.get(name)
    if old is None or update:
        snapshots[name] = rendered
        return None
    if old == rendered:
        return None
    diff = difflib.unified_diff(old.splitlines(), rendered.splitlines(), f"{name} (snapshot)", f"{name} (new)",
                                lineterm="")
    return "\n".join(diff)


snaps: dict[str, str] = {}
v1 = "System: be concise.\nAnswer from sources."
assert check_snapshot("policy_qa", v1, snaps) is None
assert check_snapshot("policy_qa", v1, snaps) is None
diff = check_snapshot("policy_qa", "System: be concise.\nAnswer ONLY from sources, with citations.", snaps)
assert "-Answer from sources." in diff and "+Answer ONLY from sources, with citations." in diff
assert check_snapshot("policy_qa", "new", snaps, update=True) is None and snaps["policy_qa"] == "new"
```

Snapshots make prompt changes explicit in pull requests. Reviewers see exactly what the model will receive, and accidental changes (a whitespace or template-engine change) don't slip through. Pair every intentional snapshot update with an evaluation run.

## Likely follow-ups

- Why can a harmless-looking whitespace change in the prompt prefix hurt cost?

---

[← Q0148](../../batch_02_prompting_context_structured_output/0148_unit_tests_for_prompts/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0150 →](../../batch_02_prompting_context_structured_output/0150_sanitise_model_markdown_before_rendering/README.md)
