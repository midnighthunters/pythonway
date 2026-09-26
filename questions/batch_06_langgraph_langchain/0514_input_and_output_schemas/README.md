# Q0514 · Input and output schemas

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Graph API | Medium |

## Question

Use separate input and output schemas so callers only send a question and only receive an answer, while internal scratch fields stay private to the graph.

## Answer

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class Input(TypedDict):
    question: str


class Output(TypedDict):
    answer: str


class Internal(TypedDict):
    question: str
    retrieved: list[str]
    answer: str


def retrieve(state: Internal) -> dict:
    return {"retrieved": ["[1] London hotels capped at 180 GBP"]}


def answer(state: Internal) -> dict:
    return {"answer": f"The cap is 180 GBP {state['retrieved'][0][:3]}"}


b = StateGraph(Internal, input_schema=Input, output_schema=Output)
b.add_node("retrieve", retrieve)
b.add_node("answer", answer)
b.add_edge(START, "retrieve")
b.add_edge("retrieve", "answer")
b.add_edge("answer", END)
out = b.compile().invoke({"question": "London hotel cap?"})
assert out == {"answer": "The cap is 180 GBP [1]"}
```

Output schemas keep internal details (retrieved chunks, scores, prompts) from leaking to API callers, which matters for data minimisation and stable API contracts. Input schemas document exactly what callers must provide.

## Likely follow-ups

- How would you expose the retrieved sources to the UI but not to other callers?

---

[← Q0513](../../batch_06_langgraph_langchain/0513_parallel_branches_and_supersteps/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0515 →](../../batch_06_langgraph_langchain/0515_pydantic_state_validation/README.md)
