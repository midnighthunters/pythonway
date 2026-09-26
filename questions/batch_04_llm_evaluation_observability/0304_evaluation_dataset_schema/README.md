# Q0304 · Evaluation dataset schema

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Datasets | Medium |

## Question

Define a validated schema for evaluation cases (id, input, expected answer or behaviour, relevant documents, tags) and a JSONL loader that rejects duplicate ids and inconsistent cases.

## Answer

```python
import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EvalCase(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(pattern=r"^[a-z0-9_-]+$")
    input: str = Field(min_length=1)
    expected: str | None = None
    expected_behavior: Literal["answer", "abstain", "refuse"] = "answer"
    relevant_doc_ids: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    persona: str = "employee"

    @model_validator(mode="after")
    def consistent(self) -> "EvalCase":
        if self.expected_behavior == "answer" and not (self.expected or self.relevant_doc_ids):
            raise ValueError("answer cases need an expected answer or relevant documents")
        if self.expected_behavior != "answer" and self.expected:
            raise ValueError("abstain/refuse cases must not have an expected answer")
        return self


def load_cases(jsonl: str) -> list[EvalCase]:
    cases, seen = [], set()
    for n, line in enumerate(jsonl.splitlines(), 1):
        if not line.strip():
            continue
        case = EvalCase.model_validate(json.loads(line))
        if case.id in seen:
            raise ValueError(f"line {n}: duplicate id {case.id}")
        seen.add(case.id)
        cases.append(case)
    return cases


data = "\n".join([
    '{"id": "hotel_cap_london", "input": "London hotel cap?", "expected": "180 GBP", "tags": ["policy"]}',
    '{"id": "unanswerable_1", "input": "CEO bonus?", "expected_behavior": "abstain"}',
])
cases = load_cases(data)
assert [c.id for c in cases] == ["hotel_cap_london", "unanswerable_1"] and cases[0].tags == ("policy",)
for bad in ('{"id": "x", "input": "q"}', '{"id": "a", "input": "q", "expected": "y"}\n{"id": "a", "input": "q", "expected": "z"}'):
    try:
        load_cases(bad)
        raise AssertionError(bad)
    except ValueError:
        pass
```

Version the dataset (a git or DVC hash in every evaluation report), keep a changelog, and store the provenance of each case (where it came from, who labelled it, when).

## Likely follow-ups

- What metadata would let you slice results usefully later?

---

[← Q0303](../../batch_04_llm_evaluation_observability/0303_define_success_criteria_before_building/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0305 →](../../batch_04_llm_evaluation_observability/0305_exact_and_normalised_match/README.md)
