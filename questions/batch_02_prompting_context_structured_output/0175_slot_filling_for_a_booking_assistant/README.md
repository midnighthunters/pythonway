# Q0175 · Slot filling for a booking assistant

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Conversation design | Medium |

## Question

Implement a small slot-filling flow for booking a meeting room: collect the required slots from extracted values across turns, validate them, ask for what's missing, confirm, and only book after an explicit "yes".

## Answer

```python
class BookingFlow:
    REQUIRED = ("room", "date", "attendees")

    def __init__(self) -> None:
        self.slots: dict[str, object] = {}
        self.state = "collecting"
        self.booked: dict | None = None

    def _merge(self, extracted: dict) -> None:
        for k, v in extracted.items():
            if k == "attendees" and v is not None and not (isinstance(v, int) and 1 <= v <= 20):
                continue
            if k in self.REQUIRED and v not in (None, ""):
                self.slots[k] = v

    def handle(self, extracted: dict, user_text: str) -> str:
        if self.state == "confirming":
            if user_text.strip().lower() in {"yes", "y", "confirm"}:
                self.state, self.booked = "done", dict(self.slots)
                return "Booked."
            self.state = "collecting"
        self._merge(extracted)
        missing = [s for s in self.REQUIRED if s not in self.slots]
        if missing:
            return f"What {missing[0]} would you like?"
        self.state = "confirming"
        return f"Book {self.slots['room']} on {self.slots['date']} for {self.slots['attendees']}? (yes/no)"


flow = BookingFlow()
assert flow.handle({"room": "Thames 3"}, "Book Thames 3") == "What date would you like?"
assert flow.handle({"date": "2026-10-02", "attendees": 99}, "Friday, for 99") == "What attendees would you like?"
assert flow.handle({"attendees": 6}, "six of us").startswith("Book Thames 3 on 2026-10-02 for 6?")
assert flow.handle({"date": "2026-10-03"}, "no, Saturday").startswith("Book Thames 3 on 2026-10-03")
assert flow.handle({}, "yes") == "Booked." and flow.booked["date"] == "2026-10-03"
```

The LLM's job is extraction (turning free text into slot values). The state machine, validation and the confirmation gate stay in code, where they are testable and can't be talked around.

## Likely follow-ups

- How would you let the LLM handle unexpected detours ("actually, what rooms have a screen?") without losing state?

---

[← Q0174](../../batch_02_prompting_context_structured_output/0174_when_to_ask_a_clarifying_question/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0176 →](../../batch_02_prompting_context_structured_output/0176_style_guide_compliance/README.md)
