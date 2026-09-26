# Q0132 · Money and dates in structured output

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

Extracted amounts arrive as strings such as "1,234.50" or "£1,234.50", and dates in ISO format. Write Pydantic validators that normalise amounts to Decimal, reject floats (to avoid binary rounding), and restrict currency to an allowlist.

## Answer

```python
from datetime import date
from decimal import Decimal, InvalidOperation

from pydantic import BaseModel, ValidationError, field_validator

ALLOWED_CCY = {"GBP", "USD", "EUR"}


class Payment(BaseModel):
    amount: Decimal
    currency: str
    value_date: date

    @field_validator("amount", mode="before")
    @classmethod
    def parse_amount(cls, v):
        if isinstance(v, float):
            raise ValueError("send amounts as strings, not floats")
        if isinstance(v, str):
            cleaned = v.strip().lstrip("£$€").replace(",", "")
            try:
                v = Decimal(cleaned)
            except InvalidOperation as e:
                raise ValueError(f"not a number: {v!r}") from e
        return v

    @field_validator("amount")
    @classmethod
    def two_dp(cls, v: Decimal) -> Decimal:
        if v.as_tuple().exponent < -2:
            raise ValueError("more than 2 decimal places")
        return v.quantize(Decimal("0.01"))

    @field_validator("currency")
    @classmethod
    def known_ccy(cls, v: str) -> str:
        v = v.upper()
        if v not in ALLOWED_CCY:
            raise ValueError(f"unsupported currency {v}")
        return v


p = Payment.model_validate({"amount": "£1,234.5", "currency": "gbp", "value_date": "2026-10-01"})
assert p.amount == Decimal("1234.50") and str(p.amount) == "1234.50" and p.currency == "GBP"
for bad in ({"amount": 12.3, "currency": "GBP", "value_date": "2026-10-01"},
            {"amount": "1.234", "currency": "GBP", "value_date": "2026-10-01"},
            {"amount": "ten", "currency": "GBP", "value_date": "2026-10-01"},
            {"amount": "10", "currency": "JPY", "value_date": "2026-10-01"}):
    try:
        Payment.model_validate(bad)
        raise AssertionError(bad)
    except ValidationError:
        pass
```

Locale caution: "1.234,50" means 1234.50 in much of Europe. Either ask the model to normalise to a canonical format in the schema description, or detect the locale explicitly. Never guess silently with financial values.

## Likely follow-ups

- How would you handle amounts in European formats safely?

---

[← Q0131](../../batch_02_prompting_context_structured_output/0131_nullable_versus_missing_fields/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0133 →](../../batch_02_prompting_context_structured_output/0133_parse_partial_json_while_streaming/README.md)
