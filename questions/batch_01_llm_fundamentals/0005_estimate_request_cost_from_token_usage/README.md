# Q0005 · Estimate request cost from token usage

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Cost | Easy |

## Question

Write a function that computes the cost of an LLM call from input, cached-input and output token counts, given per-million-token prices. It must be exact for billing (no float drift) and reject negative counts.

## Answer

Why it matters here: LLM Suite has to charge back usage to business units. Cost per request is also a core SLO alongside latency.

```python
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

MILLION = Decimal(1_000_000)


@dataclass(frozen=True)
class Price:
    input_per_m: Decimal
    output_per_m: Decimal
    cached_input_per_m: Decimal | None = None


def request_cost(price: Price, input_tokens: int, output_tokens: int, cached_tokens: int = 0) -> Decimal:
    if min(input_tokens, output_tokens, cached_tokens) < 0 or cached_tokens > input_tokens:
        raise ValueError("invalid token counts")
    cached_rate = price.cached_input_per_m if price.cached_input_per_m is not None else price.input_per_m
    total = ((input_tokens - cached_tokens) * price.input_per_m
             + cached_tokens * cached_rate
             + output_tokens * price.output_per_m) / MILLION
    return total.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


p = Price(Decimal("2.50"), Decimal("10.00"), Decimal("1.25"))
assert request_cost(p, 1_000_000, 0) == Decimal("2.500000")
assert request_cost(p, 10_000, 500) == Decimal("0.030000")
assert request_cost(p, 10_000, 500, cached_tokens=8_000) == Decimal("0.020000")
try:
    request_cost(p, 10, 5, cached_tokens=20)
    raise AssertionError
except ValueError:
    pass
```

The prices here are illustrative, not current list prices.

Notes: output tokens are typically priced several times higher than input tokens, and reasoning models also bill hidden reasoning tokens as output. Use `Decimal` or integer micro-units for money.

## Likely follow-ups

- How would you attribute cost when one user request triggers five LLM calls and three tool calls in an agent?
- Where do you get authoritative token counts (the provider's `usage` field versus your own tokenizer)?

---

[← Q0004](../../batch_01_llm_fundamentals/0004_encode_text_with_learned_bpe_merges/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0006 →](../../batch_01_llm_fundamentals/0006_what_embeddings_are/README.md)
