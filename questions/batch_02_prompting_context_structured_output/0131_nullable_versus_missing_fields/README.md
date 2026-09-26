# Q0131 · Nullable versus missing fields

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

In extraction, "the document says there is no due date" and "we didn't find a due date field" are different. Model this in Pydantic and show how to distinguish an explicit null from an omitted field.

## Answer

```python
from datetime import date

from pydantic import BaseModel


class InvoiceFields(BaseModel):
    invoice_number: str
    due_date: date | None = None
    po_number: str | None = None


explicit = InvoiceFields.model_validate_json('{"invoice_number": "INV-1", "due_date": null}')
omitted = InvoiceFields.model_validate_json('{"invoice_number": "INV-1"}')
assert explicit.due_date is None and omitted.due_date is None
assert "due_date" in explicit.model_fields_set and "due_date" not in omitted.model_fields_set
assert explicit.model_dump(exclude_unset=True) == {"invoice_number": "INV-1", "due_date": None}
```

Design choices:
- In the schema description, tell the model when to use null ("null if the document states no due date or none is present").
- For richer semantics, use an explicit status such as `due_date_status: Literal["found", "not_present", "unreadable"]`. This is better for downstream business logic and evaluation.
- With strict structured outputs every field is required, so you only get explicit nulls. The status-field pattern then becomes the way to express why a value is missing.

## Likely follow-ups

- Why is an explicit status field better for analytics than null?

---

[← Q0130](../../batch_02_prompting_context_structured_output/0130_constrain_classification_labels_with_literal/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0132 →](../../batch_02_prompting_context_structured_output/0132_money_and_dates_in_structured_output/README.md)
