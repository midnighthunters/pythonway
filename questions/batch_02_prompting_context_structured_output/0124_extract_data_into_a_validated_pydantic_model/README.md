# Q0124 · Extract data into a validated Pydantic model

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

Define a Pydantic v2 model for extracting a card transaction (merchant, amount as Decimal with 2 decimal places and above 0, ISO currency code, date), and show validation catching bad model output.

## Answer

```python
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class Transaction(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    merchant: str = Field(min_length=1, max_length=120)
    amount: Decimal = Field(gt=0, decimal_places=2)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    booked_on: date


ok = Transaction.model_validate_json(
    '{"merchant": " Pret A Manger ", "amount": "4.95", "currency": "GBP", "booked_on": "2026-09-25"}')
assert ok.merchant == "Pret A Manger" and ok.amount == Decimal("4.95") and ok.booked_on.day == 25

bad_outputs = [
    '{"merchant": "X", "amount": "4.955", "currency": "GBP", "booked_on": "2026-09-25"}',
    '{"merchant": "X", "amount": "-1", "currency": "GBP", "booked_on": "2026-09-25"}',
    '{"merchant": "X", "amount": "1.00", "currency": "gbp", "booked_on": "2026-09-25"}',
    '{"merchant": "X", "amount": "1.00", "currency": "GBP", "booked_on": "25/09/2026"}',
    '{"merchant": "X", "amount": "1.00", "currency": "GBP", "booked_on": "2026-09-25", "note": "hi"}',
]
for raw in bad_outputs:
    try:
        Transaction.model_validate_json(raw)
        raise AssertionError(raw)
    except ValidationError:
        pass
```

Money as a string-encoded Decimal avoids float rounding. `extra="forbid"` catches invented fields. The ValidationError messages are precise enough to feed back to the model for a retry.

## Likely follow-ups

- How do you present validation errors back to the model in a retry prompt?

---

[← Q0123](../../batch_02_prompting_context_structured_output/0123_json_mode_structured_outputs_and_function_calling/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0125 →](../../batch_02_prompting_context_structured_output/0125_generate_a_json_schema_from_a_pydantic_model/README.md)
