# Q0767 · Provisioned Throughput cost vs On-Demand breakeven calculator

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Write Python code that calculates the cost breakeven point between Amazon Bedrock On-Demand token pricing and 1-month Provisioned Throughput commitment.

## Answer

```python
from typing import Dict


def calculate_bedrock_breakeven(
    monthly_provisioned_cost_usd: float,
    input_price_per_k: float,
    output_price_per_k: float,
    input_to_output_ratio: float = 3.0,
) -> Dict[str, float]:
    # Blended price per 1k tokens based on ratio (e.g. 3 input tokens for every 1 output token)
    weight_input = input_to_output_ratio / (input_to_output_ratio + 1.0)
    weight_output = 1.0 / (input_to_output_ratio + 1.0)
    blended_per_k = (weight_input * input_price_per_k) + (weight_output * output_price_per_k)

    # Total tokens needed in a month to break even
    breakeven_tokens = (monthly_provisioned_cost_usd / blended_per_k) * 1000.0
    daily_tokens = breakeven_tokens / 30.0

    return {
        "monthly_breakeven_tokens": round(breakeven_tokens),
        "daily_breakeven_tokens": round(daily_tokens),
        "blended_price_per_k": round(blended_per_k, 5),
    }


# Example: $14,000/month provisioned unit; On-demand: $0.003 input / $0.015 output
res = calculate_bedrock_breakeven(
    monthly_provisioned_cost_usd=14000.0,
    input_price_per_k=0.003,
    output_price_per_k=0.015,
    input_to_output_ratio=3.0,
)

assert res["monthly_breakeven_tokens"] > 0
assert res["daily_breakeven_tokens"] > 0
assert res["blended_price_per_k"] == 0.006
```

## Likely follow-ups

- How does the ratio of prompt tokens to completion tokens affect the breakeven calculation?
- How does traffic burstiness influence the decision beyond pure cost breakeven?

---

[← Q0766](../../batch_08_azure_openai_bedrock_cloud_ai/0766_amazon_bedrock_provisioned_throughput_model_units_and/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0768 →](../../batch_08_azure_openai_bedrock_cloud_ai/0768_custom_model_import_in_amazon_bedrock/README.md)
