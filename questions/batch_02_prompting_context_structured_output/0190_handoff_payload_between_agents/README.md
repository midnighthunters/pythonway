# Q0190 · Handoff payload between agents

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Multi-agent | Medium |

## Question

In a supervisor or multi-agent system, define a validated handoff message: source and target agent, the task, a bounded context summary, key facts, and open questions. Reject unknown agents and self-handoffs.

## Answer

```python
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

AGENTS = {"supervisor", "payments_agent", "policy_agent", "human_review"}


class Handoff(BaseModel):
    model_config = ConfigDict(extra="forbid")

    from_agent: str
    to_agent: str
    task: str = Field(min_length=5)
    context_summary: str = Field(max_length=500)
    facts: dict[str, str] = {}
    open_questions: list[str] = []

    @field_validator("from_agent", "to_agent")
    @classmethod
    def known_agent(cls, v: str) -> str:
        if v not in AGENTS:
            raise ValueError(f"unknown agent {v!r}")
        return v

    @model_validator(mode="after")
    def no_self_handoff(self) -> "Handoff":
        if self.from_agent == self.to_agent:
            raise ValueError("agent cannot hand off to itself")
        return self


h = Handoff(from_agent="supervisor", to_agent="policy_agent", task="Find the UK hotel cap",
            context_summary="User travelling to London next week.", facts={"city": "London"})
assert h.to_agent == "policy_agent"
for bad in ({"to_agent": "shell_agent"}, {"to_agent": "supervisor"}, {"context_summary": "x" * 501}):
    try:
        Handoff(**{**h.model_dump(), **bad})
        raise AssertionError(bad)
    except ValidationError:
        pass
```

Passing a concise, structured handoff (rather than the whole transcript) keeps the receiving agent's context clean, limits data exposure to what it needs, and makes handoffs loggable and testable. A2A formalises the cross-service version of this with tasks, messages and artifacts.

## Likely follow-ups

- What should never be included in a handoff to a less-privileged agent?

---

[← Q0189](../../batch_02_prompting_context_structured_output/0189_validate_parallel_tool_calls_independently/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0191 →](../../batch_02_prompting_context_structured_output/0191_tell_the_model_about_tool_side_effects/README.md)
