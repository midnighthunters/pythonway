# Q0134 · Discriminated unions for agent actions

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

An agent step must return exactly one of several action types (search, transfer or ask the user), each with different fields. Model it with a Pydantic discriminated union and parse the model output.

## Answer

```python
from decimal import Decimal
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, TypeAdapter, ValidationError


class Search(BaseModel):
    action: Literal["search"]
    query: str = Field(min_length=3)


class Transfer(BaseModel):
    action: Literal["transfer"]
    amount: Decimal = Field(gt=0)
    to_account: str = Field(pattern=r"^[A-Z0-9-]{6,34}$")


class AskUser(BaseModel):
    action: Literal["ask_user"]
    question: str


Action = Annotated[Union[Search, Transfer, AskUser], Field(discriminator="action")]
adapter = TypeAdapter(Action)

a = adapter.validate_json('{"action": "transfer", "amount": "250.00", "to_account": "GB-SAVINGS-01"}')
assert isinstance(a, Transfer) and a.amount == Decimal("250.00")
assert isinstance(adapter.validate_json('{"action": "ask_user", "question": "Which account?"}'), AskUser)
for bad in ('{"action": "delete_all"}', '{"action": "transfer", "amount": "-5", "to_account": "GB-SAV-01"}'):
    try:
        adapter.validate_json(bad)
        raise AssertionError(bad)
    except ValidationError:
        pass
```

The discriminator gives precise errors (it validates against the chosen variant only) and fast dispatch. Downstream, a `match` statement on the type keeps the handlers explicit. Side-effecting variants such as `Transfer` should still go through authorisation and user confirmation. Parsing successfully doesn't mean the action is permitted.

## Likely follow-ups

- How does this compare with exposing each action as a separate tool?

---

[← Q0133](../../batch_02_prompting_context_structured_output/0133_parse_partial_json_while_streaming/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0135 →](../../batch_02_prompting_context_structured_output/0135_cross_field_validation_of_extracted_invoices/README.md)
