# Q0174 · When to ask a clarifying question

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Conversation design | Medium |

## Question

Write the decision logic for an assistant: given the extracted slots and the options for each (for example the user's accounts), either auto-fill an unambiguous slot, ask a targeted clarifying question, or proceed.

## Answer

```python
def clarify(slots: dict, required: list[str], options: dict[str, list[str]]) -> str | None:
    for name in required:
        value, choices = slots.get(name), options.get(name, [])
        label = name.replace("_", " ")
        if value is None:
            if len(choices) == 1:
                slots[name] = choices[0]
                continue
            return f"Which {label}?" + (f" Options: {', '.join(choices)}." if choices else "")
        if choices and value not in choices:
            return f"I couldn't find {label} {value!r}. Options: {', '.join(choices)}."
    return None


opts = {"from_account": ["Current ****1234", "Savings ****9876"], "currency": ["GBP"]}
slots = {"amount": "200"}
assert clarify(slots, ["amount", "from_account", "currency"], opts) == (
    "Which from account? Options: Current ****1234, Savings ****9876.")
slots["from_account"] = "Savings ****9876"
assert clarify(slots, ["amount", "from_account", "currency"], opts) is None and slots["currency"] == "GBP"
assert clarify({"amount": "5", "from_account": "ISA"}, ["amount", "from_account"], opts).startswith("I couldn't find")
```

Principles: ask only when an answer would change the action, ask one targeted question at a time with the options listed, auto-fill when there is exactly one valid option, and always confirm before irreversible actions. Over-asking frustrates users, and guessing on money is unacceptable.

## Likely follow-ups

- When is it acceptable to proceed with a sensible default instead of asking?

---

[← Q0173](../../batch_02_prompting_context_structured_output/0173_handle_refusals_in_structured_output/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0175 →](../../batch_02_prompting_context_structured_output/0175_slot_filling_for_a_booking_assistant/README.md)
