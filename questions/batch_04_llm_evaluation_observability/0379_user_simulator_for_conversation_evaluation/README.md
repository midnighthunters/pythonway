# Q0379 · User simulator for conversation evaluation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Conversation evaluation | Hard |

## Question

Implement a simple goal-driven user simulator for a booking assistant: the simulator answers the assistant's questions from a hidden goal, and the harness scores task success (correct booking) and the number of turns.

## Answer

```python
from typing import Callable


def simulate(assistant: Callable[[list[dict]], dict], goal: dict, max_turns: int = 8) -> dict:
    history = [{"role": "user", "text": f"I need a meeting room in {goal['city']}."}]
    for turn in range(1, max_turns + 1):
        reply = assistant(history)
        history.append({"role": "assistant", "text": reply["text"]})
        if reply.get("booking") is not None:
            return {"success": reply["booking"] == goal, "turns": turn, "history": history}
        asked = reply.get("asks")
        answer = str(goal.get(asked, "I don't know")) if asked else "Yes, please go ahead."
        history.append({"role": "user", "text": answer, "slot": asked})
    return {"success": False, "turns": max_turns, "history": history}


def make_assistant(bug: bool = False):
    def assistant(history: list[dict]) -> dict:
        slots = {"city": "London"}
        for m in history:
            if m.get("slot"):
                slots[m["slot"]] = int(m["text"]) if m["slot"] == "people" else m["text"]
        for need in ("date", "people"):
            if need not in slots:
                return {"text": f"What {need}?", "asks": need}
        if bug:
            slots["people"] = slots["people"] + 1
        return {"text": "Booked.", "booking": slots}
    return assistant


goal = {"city": "London", "date": "2026-10-02", "people": 6}
ok = simulate(make_assistant(), goal)
assert ok["success"] and ok["turns"] == 3
assert not simulate(make_assistant(bug=True), goal)["success"]
```

In real harnesses, the simulator is an LLM prompted with the persona and goal (sometimes impatient, vague or changing its mind), and success is checked against the final environment state. Run many goals per persona, and watch for the simulator "helping" the assistant by volunteering information it wasn't asked for.

## Likely follow-ups

- How would you make the simulated user realistically vague or inconsistent?

---

[← Q0378](../../batch_04_llm_evaluation_observability/0378_evaluating_multi_turn_conversations/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0380 →](../../batch_04_llm_evaluation_observability/0380_evaluating_memory_and_personalisation/README.md)
