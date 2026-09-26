# Q0784 · Cost vs quality routing engine in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

Write Python code implementing a rule-based complexity router that assigns incoming prompts to `low_cost`, `standard`, or `frontier` model tiers.

## Answer

```python
from typing import Dict


class ModelTierRouter:
    @staticmethod
    def route_prompt(prompt: str, requires_math: bool = False) -> str:
        text_len = len(prompt)
        prompt_lower = prompt.lower()

        # Complex reasoning / legal / math triggers frontier tier
        if requires_math or any(k in prompt_lower for k in ["reconcile", "covenant breach", "derivative pricing", "legal clause"]):
            return "frontier_model"

        # Standard RAG / summarization
        if text_len > 300 or "summarize" in prompt_lower or "explain" in prompt_lower:
            return "standard_model"

        # Simple classification / lookups
        return "low_cost_model"


assert ModelTierRouter.route_prompt("Classify sentiment: Great earnings", requires_math=False) == "low_cost_model"
assert ModelTierRouter.route_prompt("Summarize the attached 10-K report filing in 3 paragraphs.") == "standard_model"
assert ModelTierRouter.route_prompt("Calculate derivative pricing and check covenant breach.", requires_math=True) == "frontier_model"
```

## Likely follow-ups

- How can user feedback ("Regenerate with more detail") dynamically escalate the model tier?
- What metrics track whether lower-cost models meet task-specific accuracy benchmarks?

---

[← Q0783](../../batch_08_azure_openai_bedrock_cloud_ai/0783_cost_arbitrage_routing_non_critical_tasks_to_lowest_cost/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0785 →](../../batch_08_azure_openai_bedrock_cloud_ai/0785_streaming_sse_proxy_with_backpressure_handling/README.md)
