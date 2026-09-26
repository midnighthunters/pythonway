# Q0332 · Key-point coverage metric

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Summarisation evaluation | Easy |

## Question

Implement key-point coverage: each expected key point has required keywords (with alternatives), and a point counts as covered if the summary contains one alternative for every required keyword group.

## Answer

```python
import re


def covered(summary: str, keyword_groups: list[list[str]]) -> bool:
    text = summary.lower()
    return all(any(re.search(rf"\b{re.escape(alt.lower())}\b", text) for alt in group) for group in keyword_groups)


def key_point_coverage(summary: str, key_points: dict[str, list[list[str]]]) -> tuple[float, list[str]]:
    missing = [name for name, groups in key_points.items() if not covered(summary, groups)]
    return 1 - len(missing) / len(key_points), missing


points = {
    "decision": [["approved", "signed off"], ["budget"]],
    "owner": [["priya"]],
    "deadline": [["friday", "3 october", "2026-10-03"]],
}
summary = "The committee signed off the budget. Tom will circulate minutes by Friday."
score, missing = key_point_coverage(summary, points)
assert abs(score - 2 / 3) < 1e-12 and missing == ["owner"]
```

Keyword coverage is cheap and deterministic, which makes it good for CI. Its weakness is paraphrase ("green-lit"), so add alternatives or use a judge for "is key point X present?". The list of missing points is the useful debugging output.

## Likely follow-ups

- How would you generate key points for 500 documents without SMEs writing them all?

---

[← Q0331](../../batch_04_llm_evaluation_observability/0331_evaluating_summarisation/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0333 →](../../batch_04_llm_evaluation_observability/0333_evaluating_tool_calling_accuracy/README.md)
