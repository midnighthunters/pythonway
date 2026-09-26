# Q0845 · FinOps cost metering: Calculating USD cost per request by model

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Rate limiting and quotas | Easy |

## Question

Write Python code that calculates the financial USD cost of an LLM completion based on provider pricing tables (input tokens, cached input tokens, output tokens).

## Answer

Enterprise GenAI platforms must perform precise chargeback to departments. Different foundation models (GPT-4o, Claude 3.5 Sonnet, Llama-3-70B) charge differentiated rates per million tokens.

```python
from typing import Dict


PRICING_CATALOG = {
    "gpt-4o": {
        "input_per_million": 2.50,
        "cached_input_per_million": 1.25,
        "output_per_million": 10.00,
    },
    "claude-3-5-sonnet": {
        "input_per_million": 3.00,
        "cached_input_per_million": 0.30,
        "output_per_million": 15.00,
    },
}


def calculate_cost_usd(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cached_input_tokens: int = 0,
) -> float:
    rates = PRICING_CATALOG.get(model)
    if not rates:
        raise ValueError(f"Unknown model: {model}")

    uncached_input = max(0, input_tokens - cached_input_tokens)
    cost = (
        (uncached_input / 1_000_000 * rates["input_per_million"])
        + (cached_input_tokens / 1_000_000 * rates["cached_input_per_million"])
        + (output_tokens / 1_000_000 * rates["output_per_million"])
    )
    return round(cost, 6)


# 10,000 input tokens (5,000 cached) and 1,000 output tokens on GPT-4o
cost = calculate_cost_usd(
    model="gpt-4o",
    input_tokens=10_000,
    cached_input_tokens=5_000,
    output_tokens=1_000,
)
# Expected: (5000 * 2.50 + 5000 * 1.25 + 1000 * 10.00) / 1,000,000
# = (0.0125 + 0.00625 + 0.0100) = 0.02875 USD
assert cost == 0.02875
```

## Likely follow-ups

- How do prompt caching discounts alter FinOps cost optimization strategies in agent loops?
- How are embedding models priced compared to text generation models?

---

[← Q0844](../../batch_09_genai_services_fastapi/0844_per_request_token_budgeting_and_hard_cutoff_limits_in/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0846 →](../../batch_09_genai_services_fastapi/0846_asynchronous_usage_event_publishing_to_kafka_for_enterprise/README.md)
