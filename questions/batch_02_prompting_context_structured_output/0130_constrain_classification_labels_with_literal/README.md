# Q0130 · Constrain classification labels with Literal

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Easy |

## Question

Use a Pydantic model with a `Literal` label and a short reason field for an intent classifier, and show that invented labels are rejected.

## Answer

```python
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

Intent = Literal["balance_query", "card_block", "dispute", "other"]


class IntentResult(BaseModel):
    intent: Intent
    reason: str = Field(max_length=150)


r = IntentResult.model_validate_json('{"intent": "card_block", "reason": "User reports stolen card"}')
assert r.intent == "card_block"
try:
    IntentResult.model_validate_json('{"intent": "fraud", "reason": "x"}')
    raise AssertionError
except ValidationError as e:
    assert e.errors()[0]["type"] == "literal_error"
```

Always include an escape label ("other" or "unknown"), so the model isn't forced into a wrong class. Put the `reason` field before or after the label deliberately: putting reasoning first can improve accuracy (the model "thinks" before choosing), and putting the label first reduces latency when you stream.

## Likely follow-ups

- Does field order in a schema affect model accuracy?

---

[← Q0129](../../batch_02_prompting_context_structured_output/0129_repair_common_json_errors_conservatively/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0131 →](../../batch_02_prompting_context_structured_output/0131_nullable_versus_missing_fields/README.md)
