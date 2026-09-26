# Q0164 · Generate, critique and revise loop

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Self-refinement | Medium |

## Question

Implement a generate → critique → revise loop that stops when the critic finds no issues or after N rounds, and returns the final draft plus a history for audit.

## Answer

```python
from typing import Callable


def refine_loop(task: str, generate: Callable[[str], str], critique: Callable[[str], list[str]],
                revise: Callable[[str, list[str]], str], max_rounds: int = 3) -> tuple[str, list[dict]]:
    draft = generate(task)
    history = []
    for round_no in range(1, max_rounds + 1):
        issues = critique(draft)
        history.append({"round": round_no, "issues": issues})
        if not issues:
            break
        draft = revise(draft, issues)
    return draft, history


def critic(draft: str) -> list[str]:
    issues = []
    if "[1]" not in draft:
        issues.append("missing citation")
    if len(draft) > 60:
        issues.append("too long")
    return issues


def reviser(draft: str, issues: list[str]) -> str:
    if "missing citation" in issues:
        draft += " [1]"
    if "too long" in issues:
        draft = draft[:50].rstrip() + " [1]"
    return draft


final, hist = refine_loop("summarise policy",
                          lambda t: "Employees must book travel through the approved portal in advance.",
                          critic, reviser)
assert final.endswith("[1]") and len(final) <= 60
assert [h["issues"] for h in hist] == [["missing citation", "too long"], []]
```

Self-critique helps most when the critic has concrete, checkable criteria, or better, deterministic checks (tests, validators, citation checks). Pure "is this good?" self-critique by the same model often rubber-stamps or over-edits. Cap the rounds, because each costs latency and tokens.

## Likely follow-ups

- When is a deterministic checker better than an LLM critic?

---

[← Q0163](../../batch_02_prompting_context_structured_output/0163_rubrics_and_checklists_inside_prompts/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0165 →](../../batch_02_prompting_context_structured_output/0165_check_required_sections_in_generated_reports/README.md)
