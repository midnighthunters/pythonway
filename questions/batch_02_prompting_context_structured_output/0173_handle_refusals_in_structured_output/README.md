# Q0173 · Handle refusals in structured output

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

Models sometimes refuse or can't answer, and strict schemas can hide that. Design a reply type that is either an answer with citations or a typed refusal, and dispatch on it.

## Answer

```python
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, TypeAdapter


class Answer(BaseModel):
    status: Literal["ok"]
    answer: str
    citations: list[int] = Field(min_length=1)


class Refusal(BaseModel):
    status: Literal["refused"]
    reason: Literal["out_of_scope", "policy", "insufficient_evidence"]
    message: str


Reply = TypeAdapter(Annotated[Union[Answer, Refusal], Field(discriminator="status")])


def handle(raw: str) -> str:
    reply = Reply.validate_json(raw)
    match reply:
        case Answer(answer=text, citations=c):
            return f"{text} (sources: {', '.join(map(str, c))})"
        case Refusal(reason="insufficient_evidence", message=m):
            return f"{m} Try the policy portal or ask HR."
        case Refusal(message=m):
            return m


assert handle('{"status": "ok", "answer": "Up to £50/night.", "citations": [1]}') == "Up to £50/night. (sources: 1)"
assert handle('{"status": "refused", "reason": "insufficient_evidence", "message": "Not in the docs."}').startswith(
    "Not in the docs.")
assert handle('{"status": "refused", "reason": "policy", "message": "I can\'t help with that."}') == "I can't help with that."
```

Without a refusal branch, a strict schema can force the model to fabricate an answer to satisfy the format. Some provider APIs also return a separate refusal field when they decline, so check it before parsing. Track refusal rates by reason as a quality metric.

## Likely follow-ups

- What would a spike in `insufficient_evidence` refusals tell you?

---

[← Q0172](../../batch_02_prompting_context_structured_output/0172_structured_plans_with_dependency_validation/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0174 →](../../batch_02_prompting_context_structured_output/0174_when_to_ask_a_clarifying_question/README.md)
