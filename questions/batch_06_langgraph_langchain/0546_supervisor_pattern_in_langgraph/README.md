# Q0546 · Supervisor pattern in LangGraph

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Multi-agent | Medium |

## Question

Implement a supervisor graph in which a supervisor node routes to worker nodes with `Command`, and workers report back until the supervisor decides the task is done.

## Answer

```python
import operator
from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command


class State(TypedDict):
    task: str
    notes: Annotated[list[str], operator.add]


def supervisor(state: State) -> Command[Literal["researcher", "writer", "__end__"]]:
    done = {n.split(":")[0] for n in state["notes"]}
    if "researcher" not in done:
        return Command(goto="researcher")
    if "writer" not in done:
        return Command(goto="writer")
    return Command(goto=END)


def researcher(state: State) -> Command[Literal["supervisor"]]:
    return Command(goto="supervisor", update={"notes": ["researcher: London cap 180 GBP [pol-7]"]})


def writer(state: State) -> Command[Literal["supervisor"]]:
    fact = state["notes"][0].split(": ", 1)[1]
    return Command(goto="supervisor", update={"notes": [f"writer: Draft - {fact}"]})


b = StateGraph(State)
b.add_node("supervisor", supervisor)
b.add_node("researcher", researcher)
b.add_node("writer", writer)
b.add_edge(START, "supervisor")
out = b.compile().invoke({"task": "Note on London hotel cap", "notes": []})
assert out["notes"] == ["researcher: London cap 180 GBP [pol-7]", "writer: Draft - London cap 180 GBP [pol-7]"]
```

In a real system, the supervisor is an LLM choosing the next worker with a structured output (an enum of worker names plus FINISH), and the workers are agents themselves (often `create_agent` subgraphs). Keep a round limit, pass summaries rather than full transcripts, and log every routing decision.

## Likely follow-ups

- How would you stop the supervisor from looping between the same two workers?

---

[← Q0545](../../batch_06_langgraph_langchain/0545_remaining_steps_for_graceful_stops/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0547 →](../../batch_06_langgraph_langchain/0547_handoffs_between_agents_with_command/README.md)
