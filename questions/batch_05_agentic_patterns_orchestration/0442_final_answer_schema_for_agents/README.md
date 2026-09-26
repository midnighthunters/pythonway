# Q0442 · Final answer schema for agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Structured output | Medium |

## Question

Define a structured final answer for an agent: the answer text, evidence tied to real tool-call ids, the actions taken, and a confidence level. Validate that the evidence references calls that actually happened.

## Answer

```python
from typing import Literal

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class Evidence(BaseModel):
    tool_call_id: str
    quote: str = Field(min_length=3)


class AgentAnswer(BaseModel):
    answer: str
    evidence: list[Evidence] = Field(min_length=1)
    actions_taken: list[str] = []
    confidence: Literal["high", "medium", "low"]

    @field_validator("evidence")
    @classmethod
    def evidence_exists(cls, v: list[Evidence], info: ValidationInfo) -> list[Evidence]:
        calls = (info.context or {}).get("tool_calls", {})
        for e in v:
            if e.tool_call_id not in calls:
                raise ValueError(f"unknown tool call {e.tool_call_id}")
            if e.quote.lower() not in calls[e.tool_call_id].lower():
                raise ValueError(f"quote not found in output of {e.tool_call_id}")
        return v


calls = {"call_1": "Booking BK-9 status: CANCELLED by airline at 06:10", "call_2": "Rebooked on LH903 dep 14:05"}
raw = {"answer": "Your 07:00 flight was cancelled; you're on LH903 at 14:05.",
       "evidence": [{"tool_call_id": "call_1", "quote": "CANCELLED by airline"},
                    {"tool_call_id": "call_2", "quote": "LH903 dep 14:05"}],
       "actions_taken": ["rebook"], "confidence": "high"}
ans = AgentAnswer.model_validate(raw, context={"tool_calls": calls})
assert ans.confidence == "high"
bad = {**raw, "evidence": [{"tool_call_id": "call_2", "quote": "LH905 dep 09:00"}]}
try:
    AgentAnswer.model_validate(bad, context={"tool_calls": calls})
    raise AssertionError
except ValueError:
    pass
```

Pydantic's validation context lets the validator check against the run's real tool outputs, so the agent can't cite evidence it never saw. This makes answers auditable and powers UI features such as "show me where this came from".

## Likely follow-ups

- How would you verify that `actions_taken` matches the action log?

---

[← Q0441](../../batch_05_agentic_patterns_orchestration/0441_choose_a_model_per_step/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0443 →](../../batch_05_agentic_patterns_orchestration/0443_stop_conditions_for_agents/README.md)
