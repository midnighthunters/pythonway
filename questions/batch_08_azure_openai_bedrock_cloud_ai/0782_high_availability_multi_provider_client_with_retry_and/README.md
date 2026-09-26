# Q0782 · High-availability multi-provider client with retry and fallback

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Hard |

## Question

Write Python code implementing a production-ready resilient LLM client that combines exponential backoff retries with multi-cloud fallback (Azure -> Bedrock).

## Answer

```python
import time
from typing import Any, Callable, Dict, List, Tuple


class ResilientMultiCloudClient:
    def __init__(self, providers: List[Tuple[str, Callable[[str], str]]], max_retries_per_provider: int = 2):
        self.providers = providers  # list of (provider_name, call_fn)
        self.max_retries = max_retries_per_provider
        self.audit_log: List[Dict[str, Any]] = []

    def execute_completion(self, prompt: str) -> Dict[str, Any]:
        for provider_name, call_fn in self.providers:
            for attempt in range(self.max_retries + 1):
                try:
                    result = call_fn(prompt)
                    self.audit_log.append({"provider": provider_name, "attempt": attempt, "status": "success"})
                    return {"provider": provider_name, "text": result}
                except Exception as exc:
                    self.audit_log.append({"provider": provider_name, "attempt": attempt, "status": "failed", "error": str(exc)})
                    if attempt < self.max_retries:
                        time.sleep(0.01)

        raise RuntimeError("All configured cloud AI providers and retries exhausted.")


# Provider 1 (Azure) fails repeatedly; Provider 2 (Bedrock) succeeds
azure_mock = lambda p: (_ for _ in ()).throw(ConnectionError("Azure 429 Quota Exceeded"))
bedrock_mock = lambda p: f"Bedrock Response to: {p}"

client = ResilientMultiCloudClient(
    providers=[("azure", azure_mock), ("bedrock", bedrock_mock)],
    max_retries_per_provider=1,
)

res = client.execute_completion("Summarize market close")
assert res["provider"] == "bedrock"
assert "Bedrock Response" in res["text"]
assert len(client.audit_log) == 3  # Azure (attempt 0, 1) + Bedrock (attempt 0)
```

## Likely follow-ups

- How does the client preserve idempotency keys when retrying across different cloud providers?
- How should streaming responses be restarted if a provider disconnects halfway through the output?

---

[← Q0781](../../batch_08_azure_openai_bedrock_cloud_ai/0781_dual_cloud_ai_gateway_architecture_azure_plus_aws_active/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0783 →](../../batch_08_azure_openai_bedrock_cloud_ai/0783_cost_arbitrage_routing_non_critical_tasks_to_lowest_cost/README.md)
