# Q0515 · Pydantic state validation

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Graph API | Medium |

## Question

Use a Pydantic model as the graph state, so inputs are validated and coerced at the graph boundary, and show a validation failure.

## Answer

```python
from pydantic import BaseModel, Field, ValidationError
from langgraph.graph import END, START, StateGraph


class RefundState(BaseModel):
    invoice_id: str = Field(pattern=r"^INV-\d+$")
    amount: float = Field(gt=0, le=10_000)
    status: str = "new"


def decide(state: RefundState) -> dict:
    return {"status": "auto_approved" if state.amount <= 100 else "needs_review"}


b = StateGraph(RefundState)
b.add_node("decide", decide)
b.add_edge(START, "decide")
b.add_edge("decide", END)
g = b.compile()
assert g.invoke({"invoice_id": "INV-7", "amount": "45"})["status"] == "auto_approved"
try:
    g.invoke({"invoice_id": "bad", "amount": 45})
    raise AssertionError
except ValidationError:
    pass
```

With a Pydantic state, nodes receive a model instance (attribute access), and inputs are validated when the graph is invoked. Trade-offs: validation adds overhead on every step, and node outputs are validated less strictly than inputs, so still validate critical values where they're produced. TypedDict is lighter and is the most common choice. Pydantic is useful at trust boundaries.

## Likely follow-ups

- Where exactly does validation happen with Pydantic state?

---

[← Q0514](../../batch_06_langgraph_langchain/0514_input_and_output_schemas/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0516 →](../../batch_06_langgraph_langchain/0516_a_react_agent_graph_with_toolnode/README.md)
