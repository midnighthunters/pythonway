# Q0758 · Custom log analytics query parser for Azure OpenAI

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

Write Python code that parses simulated Azure OpenAI JSON access logs, aggregates token consumption by model, and calculates P95 latency.

## Answer

```python
import statistics
from typing import Any, Dict, List


class LogAnalyticsParser:
    @staticmethod
    def aggregate_metrics(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        by_model = {}
        latencies = []

        for log in logs:
            model = log.get("model", "unknown")
            tokens = log.get("total_tokens", 0)
            latency = log.get("latency_ms", 0.0)

            latencies.append(latency)
            if model not in by_model:
                by_model[model] = {"total_tokens": 0, "request_count": 0}
            by_model[model]["total_tokens"] += tokens
            by_model[model]["request_count"] += 1

        latencies.sort()
        # Compute 95th percentile
        idx = int(0.95 * len(latencies))
        p95 = latencies[min(idx, len(latencies) - 1)] if latencies else 0.0

        return {"by_model": by_model, "p95_latency_ms": p95, "total_requests": len(logs)}


sample_logs = [
    {"model": "gpt-4o", "total_tokens": 1200, "latency_ms": 350.0},
    {"model": "gpt-4o", "total_tokens": 800, "latency_ms": 410.0},
    {"model": "gpt-4o-mini", "total_tokens": 300, "latency_ms": 120.0},
]

metrics = LogAnalyticsParser.aggregate_metrics(sample_logs)
assert metrics["total_requests"] == 3
assert metrics["by_model"]["gpt-4o"]["total_tokens"] == 2000
assert metrics["p95_latency_ms"] >= 350.0
```

## Likely follow-ups

- How does Kusto Query Language (KQL) express this aggregation in Azure Monitor?
- How should logs be sanitized to ensure prompts containing PII are never persisted?

---

[← Q0757](../../batch_08_azure_openai_bedrock_cloud_ai/0757_azure_monitor_and_application_insights_for_llm_latency/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0759 →](../../batch_08_azure_openai_bedrock_cloud_ai/0759_azure_openai_on_foundry_models_and_model_catalog_integration/README.md)
