# Q0599 · Rebooking workflow as a LangGraph graph

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangGraph implementation | Hard |

## Question

Implement a compact rebooking workflow: search and rank flights, pause for traveller approval with `interrupt()`, book the flight, update the hotel, and compensate (cancel the new flight) if the hotel update fails.

## Answer

```python
import operator
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    options: list[dict]
    chosen: str
    ticket: str
    hotel_ok: bool
    status: str
    log: Annotated[list[str], operator.add]


def make_graph(hotel_available: bool):
    def search(s: State) -> dict:
        return {"options": [{"id": "BA912", "score": 1.4}, {"id": "LH903", "score": 3.9}], "log": ["searched"]}

    def rank(s: State) -> dict:
        return {"chosen": max(s["options"], key=lambda o: o["score"])["id"], "log": ["ranked"]}

    def approve(s: State) -> dict:
        ok = interrupt({"question": f"Rebook onto {s['chosen']}?"})
        return {"status": "approved" if ok else "declined", "log": [f"traveller:{'yes' if ok else 'no'}"]}

    def book(s: State) -> dict:
        return {"ticket": f"TKT-{s['chosen']}", "log": [f"booked {s['chosen']}"]}

    def update_hotel(s: State) -> dict:
        return {"hotel_ok": hotel_available, "log": ["hotel updated" if hotel_available else "hotel update failed"]}

    def compensate(s: State) -> dict:
        return {"ticket": "", "status": "rolled_back", "log": [f"cancelled {s['ticket']}"]}

    def done(s: State) -> dict:
        return {"status": "rebooked", "log": ["notified traveller"]}

    b = StateGraph(State)
    for name, fn in (("search", search), ("rank", rank), ("approve", approve), ("book", book),
                     ("update_hotel", update_hotel), ("compensate", compensate), ("done", done)):
        b.add_node(name, fn)
    b.add_edge(START, "search")
    b.add_edge("search", "rank")
    b.add_edge("rank", "approve")
    b.add_conditional_edges("approve", lambda s: "book" if s["status"] == "approved" else END, ["book", END])
    b.add_edge("book", "update_hotel")
    b.add_conditional_edges("update_hotel", lambda s: "done" if s["hotel_ok"] else "compensate", ["done", "compensate"])
    b.add_edge("compensate", END)
    b.add_edge("done", END)
    return b.compile(checkpointer=InMemorySaver())


init = {"options": [], "chosen": "", "ticket": "", "hotel_ok": False, "status": "", "log": []}
happy = make_graph(hotel_available=True)
cfg = {"configurable": {"thread_id": "trip-1"}}
assert happy.invoke(init, cfg)["__interrupt__"][0].value == {"question": "Rebook onto LH903?"}
ok = happy.invoke(Command(resume=True), cfg)
assert ok["status"] == "rebooked" and ok["ticket"] == "TKT-LH903"

sad = make_graph(hotel_available=False)
cfg2 = {"configurable": {"thread_id": "trip-2"}}
sad.invoke(init, cfg2)
rolled = sad.invoke(Command(resume=True), cfg2)
assert rolled["status"] == "rolled_back" and rolled["log"][-2:] == ["hotel update failed", "cancelled TKT-LH903"]
```

This is a saga expressed as a graph: every step is checkpointed, the approval can wait indefinitely, and the compensation path is an explicit, testable branch. Real booking and cancellation tools would carry idempotency keys, and the ranking would use deterministic constraints.

## Likely follow-ups

- Where would you add a timeout for travellers who never answer?

---

[← Q0598](../../batch_06_langgraph_langchain/0598_design_a_langgraph_personal_assistant/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0600 →](../../batch_06_langgraph_langchain/0600_build_a_small_agent_end_to_end_in_an_interview/README.md)
