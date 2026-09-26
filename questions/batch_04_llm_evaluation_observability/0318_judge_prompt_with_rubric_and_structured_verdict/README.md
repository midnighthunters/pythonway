# Q0318 · Judge prompt with rubric and structured verdict

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Model-graded evaluation | Medium |

## Question

Build a judge prompt from a rubric, and parse the judge's structured verdict with validation (every rubric dimension scored 1–5, a pass/fail decision and a short rationale).

## Answer

```python
from typing import Annotated, Literal

from pydantic import BaseModel, Field, ValidationError

RUBRIC = {
    "faithfulness": "5 = every claim is supported by the sources; 1 = contradicts the sources",
    "completeness": "5 = answers all parts of the question; 1 = misses the main point",
}


class Verdict(BaseModel):
    scores: dict[str, Annotated[int, Field(ge=1, le=5)]]
    overall: Literal["pass", "fail"]
    rationale: str = Field(max_length=400)


def judge_prompt(question: str, answer: str, sources: str, rubric: dict[str, str]) -> str:
    dims = "\n".join(f"- {k}: {v}" for k, v in rubric.items())
    return (f"Evaluate the ANSWER using only the SOURCES.\nCriteria:\n{dims}\n\n"
            f"<question>{question}</question>\n<sources>{sources}</sources>\n<answer>{answer}</answer>\n"
            'Return JSON: {"scores": {criterion: 1-5}, "overall": "pass"|"fail", "rationale": "..."}')


def parse_verdict(raw: str, rubric: dict[str, str]) -> Verdict:
    v = Verdict.model_validate_json(raw)
    if set(v.scores) != set(rubric):
        raise ValueError(f"judge scored {sorted(v.scores)}, expected {sorted(rubric)}")
    return v


p = judge_prompt("Hotel cap?", "180 GBP [1]", "[1] London cap 180 GBP", RUBRIC)
assert "- faithfulness: 5 = every claim" in p and "<answer>180 GBP [1]</answer>" in p
v = parse_verdict('{"scores": {"faithfulness": 5, "completeness": 4}, "overall": "pass", "rationale": "ok"}', RUBRIC)
assert v.scores["faithfulness"] == 5
for bad in ('{"scores": {"faithfulness": 7, "completeness": 4}, "overall": "pass", "rationale": "x"}',
            '{"scores": {"faithfulness": 5}, "overall": "pass", "rationale": "x"}'):
    try:
        parse_verdict(bad, RUBRIC)
        raise AssertionError(bad)
    except (ValidationError, ValueError):
        pass
```

Treat judge outputs like any model output: validate them, count parse failures, and never let a malformed verdict silently count as a pass.

## Likely follow-ups

- Should the judge see the reference answer, and when could that bias it?

---

[← Q0317](../../batch_04_llm_evaluation_observability/0317_llm_as_judge_design/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0319 →](../../batch_04_llm_evaluation_observability/0319_pairwise_judging_with_position_swap/README.md)
