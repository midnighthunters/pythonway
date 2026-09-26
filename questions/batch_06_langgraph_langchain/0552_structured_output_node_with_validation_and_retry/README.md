# Q0552 · Structured output node with validation and retry

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Structured output | Medium |

## Question

A node asks a model for JSON, validates it with Pydantic, and loops back with the validation error (up to two retries) before failing gracefully. Implement it with a fake list model.

## Answer

```python
from typing import Literal, TypedDict

from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, ValidationError


class Route(BaseModel):
    label: Literal["it", "hr", "finance"]
    urgent: bool


model = FakeListChatModel(responses=['{"label": "legal"}', '{"label": "it", "urgent": true}'])


class State(TypedDict):
    ticket: str
    feedback: str
    attempts: int
    route: dict | None


def classify(state: State) -> dict:
    prompt = f"Classify: {state['ticket']}\n{state['feedback']}\nReturn JSON with label and urgent."
    raw = model.invoke(prompt).content
    try:
        return {"route": Route.model_validate_json(raw).model_dump(), "attempts": state["attempts"] + 1}
    except ValidationError as e:
        return {"feedback": f"Previous output invalid: {e.errors()[0]['msg']}", "attempts": state["attempts"] + 1}


def next_step(state: State) -> str:
    return END if state["route"] or state["attempts"] >= 3 else "classify"


b = StateGraph(State)
b.add_node("classify", classify)
b.add_edge(START, "classify")
b.add_conditional_edges("classify", next_step, ["classify", END])
out = b.compile().invoke({"ticket": "VPN down for trading desk", "feedback": "", "attempts": 0, "route": None})
assert out["route"] == {"label": "it", "urgent": True} and out["attempts"] == 2
```

With real providers, prefer `model.with_structured_output(Route)` (native schema enforcement), and keep the validate-and-retry loop for business rules the schema can't express. Store the attempt count and validation errors in the state for observability.

## Likely follow-ups

- Why keep validation in code even with provider-enforced schemas?

---

[← Q0551](../../batch_06_langgraph_langchain/0551_tool_errors_with_handle_tool_errors/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0553 →](../../batch_06_langgraph_langchain/0553_trim_history_before_the_model_call/README.md)
