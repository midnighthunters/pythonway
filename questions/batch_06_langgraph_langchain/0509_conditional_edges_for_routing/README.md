# Q0509 · Conditional edges for routing

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Graph API | Easy |

## Question

Add a conditional edge that routes a request to a `policy_qa` node, a `sql_analytics` node, or ends immediately for out-of-scope requests.

## Answer

```python
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    question: str
    route: str
    answer: str


def classify(state: State) -> dict:
    q = state["question"].lower()
    route = "sql" if "total" in q or "how many" in q else "policy" if "policy" in q else "out_of_scope"
    return {"route": route}


def pick_next(state: State) -> Literal["policy_qa", "sql_analytics", "__end__"]:
    return {"policy": "policy_qa", "sql": "sql_analytics"}.get(state["route"], END)


b = StateGraph(State)
b.add_node("classify", classify)
b.add_node("policy_qa", lambda s: {"answer": "Per the travel policy..."})
b.add_node("sql_analytics", lambda s: {"answer": "Total spend was..."})
b.add_edge(START, "classify")
b.add_conditional_edges("classify", pick_next, ["policy_qa", "sql_analytics", END])
b.add_edge("policy_qa", END)
b.add_edge("sql_analytics", END)
g = b.compile()
assert g.invoke({"question": "What does the travel policy say?"})["answer"].startswith("Per the travel")
assert g.invoke({"question": "How many trades last week?"})["route"] == "sql"
assert "answer" not in g.invoke({"question": "Tell me a joke"})
```

Listing the possible destinations (the third argument, or a `Literal` return type) lets LangGraph validate the graph and draw it correctly. Keep routing functions cheap and deterministic where possible, and put LLM-based classification in a node whose output the edge reads.

## Likely follow-ups

- Why put the LLM call in a node rather than inside the edge function?

---

[← Q0508](../../batch_06_langgraph_langchain/0508_remove_messages_with_removemessage/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0510 →](../../batch_06_langgraph_langchain/0510_loops_and_the_recursion_limit/README.md)
