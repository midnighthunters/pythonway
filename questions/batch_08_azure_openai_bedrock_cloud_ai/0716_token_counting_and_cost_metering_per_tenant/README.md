# Q0716 · Token counting and cost metering per tenant

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

Write Python code for an AI Gateway metering module that tracks prompt and completion tokens, calculates billing cost in USD based on model pricing, and attributes costs to client tenant IDs.

## Answer

Enterprise gateways must meter token usage for chargebacks across corporate departments (e.g. Equities, Fixed Income, Corporate Banking).

```python
from typing import Any, Dict, List


class TenantCostMeter:
    # Pricing per 1,000 tokens (USD)
    MODEL_PRICING = {
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "claude-3-5-sonnet": {"input": 0.003, "output": 0.015},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    }

    def __init__(self):
        self._tenant_usage: Dict[str, Dict[str, float]] = {}

    def record_usage(self, tenant_id: str, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        pricing = self.MODEL_PRICING.get(model, {"input": 0.005, "output": 0.015})
        input_cost = (prompt_tokens / 1000.0) * pricing["input"]
        output_cost = (completion_tokens / 1000.0) * pricing["output"]
        total_cost = round(input_cost + output_cost, 6)

        if tenant_id not in self._tenant_usage:
            self._tenant_usage[tenant_id] = {"prompt_tokens": 0, "completion_tokens": 0, "total_cost_usd": 0.0}

        self._tenant_usage[tenant_id]["prompt_tokens"] += prompt_tokens
        self._tenant_usage[tenant_id]["completion_tokens"] += completion_tokens
        self._tenant_usage[tenant_id]["total_cost_usd"] += total_cost

        return total_cost

    def get_tenant_summary(self, tenant_id: str) -> Dict[str, float]:
        return self._tenant_usage.get(tenant_id, {"prompt_tokens": 0, "completion_tokens": 0, "total_cost_usd": 0.0})


meter = TenantCostMeter()
cost1 = meter.record_usage("desk-equities", "gpt-4o", prompt_tokens=2000, completion_tokens=500)
cost2 = meter.record_usage("desk-equities", "claude-3-5-sonnet", prompt_tokens=1000, completion_tokens=200)

summary = meter.get_tenant_summary("desk-equities")
assert summary["prompt_tokens"] == 3000
assert summary["completion_tokens"] == 700
assert summary["total_cost_usd"] > 0.0
```

## Likely follow-ups

- How does token estimation with `tiktoken` allow gateways to enforce budgets before sending requests?
- How should streaming requests be metered when token counts are only known at stream completion?

---

[← Q0715](../../batch_08_azure_openai_bedrock_cloud_ai/0715_multi_provider_fallback_router_azure_openai_to_aws_bedrock/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0717 →](../../batch_08_azure_openai_bedrock_cloud_ai/0717_semantic_caching_at_the_ai_gateway_layer/README.md)
