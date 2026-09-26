# Q0718 · Weighted round-robin load balancing across cloud LLM regions

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Medium |

## Question

Implement a Weighted Round-Robin load balancer in Python that distributes LLM requests across three regional deployments based on provisioned TPM capacities.

## Answer

```python
import itertools
from typing import Dict, List


class WeightedRegionLoadBalancer:
    def __init__(self, region_weights: Dict[str, int]):
        self.region_weights = region_weights
        # Build expanded schedule based on weights
        schedule = []
        for region, weight in region_weights.items():
            schedule.extend([region] * weight)
        self._cycle = itertools.cycle(schedule)

    def get_next_region(self) -> str:
        return next(self._cycle)


# UK South has 3x capacity of East US, 2x of West Europe
balancer = WeightedRegionLoadBalancer({"uksouth": 3, "westeurope": 2, "eastus": 1})

selected = [balancer.get_next_region() for _ in range(6)]
assert selected.count("uksouth") == 3
assert selected.count("westeurope") == 2
assert selected.count("eastus") == 1
```

## Likely follow-ups

- How does weighted round-robin adapt when one region begins returning HTTP 503 Service Unavailable?
- What are the advantages of Least-Outstanding-Requests (LOR) routing over round-robin for streaming LLM calls?

---

[← Q0717](../../batch_08_azure_openai_bedrock_cloud_ai/0717_semantic_caching_at_the_ai_gateway_layer/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0719 →](../../batch_08_azure_openai_bedrock_cloud_ai/0719_streaming_responses_time_to_first_token_vs_throughput/README.md)
