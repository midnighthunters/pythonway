# Q0525 · Validate human input in an interrupt loop

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Human-in-the-loop | Medium |

## Question

Ask the user for a numeric amount with `interrupt()`, re-prompt with an explanation until the input is valid, and then continue.

## Answer

```python
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    amount: float


def ask_amount(state: State) -> dict:
    prompt = "How much should we refund (GBP)?"
    while True:
        answer = interrupt(prompt)
        try:
            value = float(answer)
            if 0 < value <= 500:
                return {"amount": value}
            prompt = f"{value} is outside the allowed range (0-500]. Please enter another amount."
        except (TypeError, ValueError):
            prompt = f"'{answer}' isn't a number. Please enter an amount such as 120.50."


b = StateGraph(State)
b.add_node("ask_amount", ask_amount)
b.add_edge(START, "ask_amount")
b.add_edge("ask_amount", END)
app = b.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "refund-ask"}}
app.invoke({"amount": 0.0}, cfg)
r1 = app.invoke(Command(resume="lots"), cfg)
assert "isn't a number" in r1["__interrupt__"][0].value
r2 = app.invoke(Command(resume="900"), cfg)
assert "outside the allowed range" in r2["__interrupt__"][0].value
assert app.invoke(Command(resume="120.5"), cfg) == {"amount": 120.5}
```

On each resume the node replays from the top: earlier `interrupt()` calls return their earlier resume values in order, and the next unanswered one pauses again. The loop therefore works, provided the code between interrupts is deterministic. Validation lives in code, not in the model.

## Likely follow-ups

- Why must the code between interrupt calls be deterministic?

---

[← Q0524](../../batch_06_langgraph_langchain/0524_nodes_re_run_from_the_start_on_resume/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0526 →](../../batch_06_langgraph_langchain/0526_static_breakpoints_with_interrupt_before/README.md)
