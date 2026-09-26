# Q0135 · Cross-field validation of extracted invoices

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

Schema enforcement guarantees shape, not arithmetic. Write a Pydantic model for an extracted invoice whose validator checks that the line items sum to the subtotal and that subtotal plus tax equals the total.

## Answer

```python
from decimal import Decimal

from pydantic import BaseModel, Field, ValidationError, model_validator


class LineItem(BaseModel):
    description: str
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0)


class Invoice(BaseModel):
    invoice_number: str
    line_items: list[LineItem] = Field(min_length=1)
    subtotal: Decimal
    tax: Decimal = Field(ge=0)
    total: Decimal

    @model_validator(mode="after")
    def check_totals(self) -> "Invoice":
        computed = sum((li.quantity * li.unit_price for li in self.line_items), Decimal("0"))
        if computed != self.subtotal:
            raise ValueError(f"subtotal {self.subtotal} != sum of line items {computed}")
        if self.subtotal + self.tax != self.total:
            raise ValueError(f"subtotal + tax = {self.subtotal + self.tax}, but total = {self.total}")
        return self


good = {"invoice_number": "INV-9", "line_items": [{"description": "Licence", "quantity": 2, "unit_price": "150.00"}],
        "subtotal": "300.00", "tax": "60.00", "total": "360.00"}
assert Invoice.model_validate(good).total == Decimal("360.00")
try:
    Invoice.model_validate({**good, "total": "3600.00"})
    raise AssertionError
except ValidationError as e:
    assert "total = 3600.00" in str(e)
```

When validation fails, you can retry with the error (the model may have misread a digit), or route the document to human review with the specific discrepancy highlighted. That is much better than silently storing inconsistent numbers.

## Likely follow-ups

- The document itself has an arithmetic error. How do you tell that apart from an extraction error?

---

[← Q0134](../../batch_02_prompting_context_structured_output/0134_discriminated_unions_for_agent_actions/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0136 →](../../batch_02_prompting_context_structured_output/0136_classification_prompt_with_label_definitions/README.md)
