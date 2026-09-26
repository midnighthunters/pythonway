# Q0184 · Extract action items from emails

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Personal assistants | Medium |

## Question

A personal assistant extracts action items from a meeting email. Define the schema (owner, task, optional due date), and accept only items whose owner is an actual participant.

## Answer

```python
from datetime import date

from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    owner: str
    task: str = Field(min_length=3, max_length=200)
    due: date | None = None


class Extraction(BaseModel):
    items: list[ActionItem] = Field(max_length=20)


def extract_actions(llm_json: str, participants: set[str]) -> tuple[list[ActionItem], list[ActionItem]]:
    items = Extraction.model_validate_json(llm_json).items
    valid = [i for i in items if i.owner in participants]
    return valid, [i for i in items if i.owner not in participants]


raw = ('{"items": [{"owner": "Priya", "task": "Send revised forecast", "due": "2026-10-02"},'
       '{"owner": "Tom", "task": "Book offsite venue"},'
       '{"owner": "Unknown Vendor", "task": "Approve invoice"}]}')
valid, rejected = extract_actions(raw, {"Priya", "Tom", "Nikhil"})
assert [(i.owner, i.due) for i in valid] == [("Priya", date(2026, 10, 2)), ("Tom", None)]
assert rejected[0].owner == "Unknown Vendor"
```

The assistant should propose the items for the user to confirm before creating tasks or sending reminders, which is a side effect on other people. Resolve owners to directory identities rather than free-text names.

## Likely follow-ups

- How would you resolve "Tom" to the right person when there are three Toms in the directory?

---

[← Q0183](../../batch_02_prompting_context_structured_output/0183_require_exact_quotes_and_verify_them/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0185 →](../../batch_02_prompting_context_structured_output/0185_chunked_extraction_over_long_documents/README.md)
