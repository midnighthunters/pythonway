# Q0736 · Implementing a Multi-LoRA adapter router in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Elastic Compute | Hard |

## Question

Write Python code for an adapter dispatch router that inspects tenant request headers and routes inference to the appropriate LoRA adapter on a shared base model.

## Answer

```python
from typing import Any, Dict


class MultiLoRARouter:
    def __init__(self, base_model_name: str):
        self.base_model = base_model_name
        # Maps domain_tag -> adapter_path
        self._adapters: Dict[str, str] = {
            "credit": "s3://models/adapters/credit_risk_v2",
            "legal": "s3://models/adapters/legal_contract_v1",
            "equities": "s3://models/adapters/equities_sentiment_v3",
        }

    def route_request(self, tenant_header: str, prompt: str) -> Dict[str, Any]:
        adapter_path = self._adapters.get(tenant_header)
        return {
            "base_model": self.base_model,
            "adapter": adapter_path,  # None implies raw base model
            "prompt": prompt,
            "status": "routed",
        }


router = MultiLoRARouter("llama-3-70b-base")
req_credit = router.route_request("credit", "Evaluate debtor covenants.")
assert req_credit["adapter"] == "s3://models/adapters/credit_risk_v2"

req_default = router.route_request("general_research", "Explain inflation.")
assert req_default["adapter"] is None
```

## Likely follow-ups

- How does adapter caching prevent reloading adapter weights from S3 on every request?
- How are tenant permissions verified before attaching a specialized financial adapter?

---

[← Q0735](../../batch_08_azure_openai_bedrock_cloud_ai/0735_multi_lora_adapter_serving_on_a_single_base_model/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0737 →](../../batch_08_azure_openai_bedrock_cloud_ai/0737_speculative_decoding_draft_model_plus_target_model/README.md)
