# Q0715 · Multi-provider fallback router: Azure OpenAI to AWS Bedrock

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Gateways | Hard |

## Question

Implement an enterprise LLM Router in Python that primary-routes to Azure OpenAI and automatically fails over to Amazon Bedrock upon unrecoverable error or persistent 429.

## Answer

High-availability financial applications cannot tolerate cloud provider outages. An AI gateway implements multi-cloud fallback:

```python
from typing import Any, Callable, Dict


class MultiCloudLLMRouter:
    def __init__(self, azure_caller: Callable[[str], str], bedrock_caller: Callable[[str], str]):
        self.azure_caller = azure_caller
        self.bedrock_caller = bedrock_caller
        self.routing_audit = []

    def complete(self, prompt: str) -> Dict[str, Any]:
        try:
            res = self.azure_caller(prompt)
            self.routing_audit.append({"provider": "azure", "status": "success"})
            return {"provider": "azure", "text": res}
        except Exception as azure_err:
            # Fallback to secondary cloud provider
            try:
                res = self.bedrock_caller(prompt)
                self.routing_audit.append({"provider": "bedrock", "status": "fallback_success", "error": str(azure_err)})
                return {"provider": "bedrock", "text": res, "fallback_from": "azure"}
            except Exception as bedrock_err:
                self.routing_audit.append({"provider": "none", "status": "all_failed"})
                raise RuntimeError(f"Both cloud AI providers failed. Azure: {azure_err}; Bedrock: {bedrock_err}")


# Test successful primary
r_ok = MultiCloudLLMRouter(azure_caller=lambda p: f"Azure: {p}", bedrock_caller=lambda p: f"Bedrock: {p}")
out_ok = r_ok.complete("Hello")
assert out_ok["provider"] == "azure"

# Test fallback on Azure 429
r_fail = MultiCloudLLMRouter(
    azure_caller=lambda p: (_ for _ in ()).throw(RuntimeError("HTTP 429: Quota Exceeded")),
    bedrock_caller=lambda p: f"Bedrock: {p}",
)
out_fail = r_fail.complete("Hello")
assert out_fail["provider"] == "bedrock"
assert "fallback_from" in out_fail
```

## Likely follow-ups

- How do you handle slight differences in output formatting between GPT-4o on Azure and Claude 3.5 on Bedrock?
- How can the router automatically probe Azure to switch back once the outage resolves?

---

[← Q0714](../../batch_08_azure_openai_bedrock_cloud_ai/0714_handling_http_429_too_many_requests_with_exponential/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0716 →](../../batch_08_azure_openai_bedrock_cloud_ai/0716_token_counting_and_cost_metering_per_tenant/README.md)
