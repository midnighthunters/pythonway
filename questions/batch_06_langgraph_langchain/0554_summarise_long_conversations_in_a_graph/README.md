# Q0554 · Summarise long conversations in a graph

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Context management | Medium |

## Question

After each answer, if the history is longer than a threshold, run a summarisation node that updates a running summary and removes old messages, keeping the last two.

## Answer

```python
from typing import TypedDict, Annotated

from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    summary: str


def answer(state: State) -> dict:
    return {"messages": [AIMessage(f"answer {len(state['messages'])}")]}


def summarize(state: State) -> dict:
    old = state["messages"][:-2]
    new_summary = (state["summary"] + " | " if state["summary"] else "") + "; ".join(
        m.content for m in old if m.type == "human")
    return {"summary": new_summary, "messages": [RemoveMessage(id=m.id) for m in old]}


b = StateGraph(State)
b.add_node("answer", answer)
b.add_node("summarize", summarize)
b.add_edge(START, "answer")
b.add_conditional_edges("answer", lambda s: "summarize" if len(s["messages"]) > 4 else END, ["summarize", END])
b.add_edge("summarize", END)
g = b.compile()
msgs = [HumanMessage("q1", id="1"), AIMessage("a1", id="2"), HumanMessage("q2", id="3"), AIMessage("a2", id="4"),
        HumanMessage("q3", id="5")]
out = g.invoke({"messages": msgs, "summary": ""})
assert out["summary"] == "q1; q2" and [m.content for m in out["messages"]] == ["q3", "answer 5"]
```

The toy summariser joins the user questions. A real one calls an LLM with the previous summary plus the dropped messages. The prompt then includes the summary as a system message. Keep exact facts (amounts, ids) in structured state rather than trusting the summary, and run summarisation asynchronously or off the critical path when possible.

## Likely follow-ups

- What facts must survive summarisation in a banking assistant?

---

[← Q0553](../../batch_06_langgraph_langchain/0553_trim_history_before_the_model_call/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0555 →](../../batch_06_langgraph_langchain/0555_visualise_a_graph_as_mermaid/README.md)
