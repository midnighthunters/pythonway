# Q0858 · Prometheus metrics endpoint for request counts, latencies, and token counters

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Medium |

## Question

Write Python code creating a custom Prometheus metrics collector in FastAPI, exporting request counts, latency histograms, and cumulative token counters on a `/metrics` route.

## Answer

Prometheus scraping enables real-time monitoring and alerting in Grafana. For GenAI services, essential metrics include:
1. `http_requests_total`: Counter by route and status code.
2. `llm_tokens_total`: Counter by model, tenant, and token type (prompt/completion).
3. `http_request_duration_seconds`: Histogram measuring latency distribution.

```python
from typing import Dict
from fastapi import FastAPI, Response
from fastapi.testclient import TestClient

app = FastAPI()


class PrometheusRegistry:
    def __init__(self):
        self.request_counts: Dict[str, int] = {}
        self.total_tokens: Dict[str, int] = {}

    def inc_request(self, endpoint: str, status_code: int) -> None:
        key = f'endpoint="{endpoint}",status="{status_code}"'
        self.request_counts[key] = self.request_counts.get(key, 0) + 1

    def inc_tokens(self, model: str, token_type: str, count: int) -> None:
        key = f'model="{model}",type="{token_type}"'
        self.total_tokens[key] = self.total_tokens.get(key, 0) + count

    def generate_prometheus_text(self) -> str:
        lines = ["# HELP http_requests_total Total HTTP requests.", "# TYPE http_requests_total counter"]
        for labels, val in self.request_counts.items():
            lines.append(f"http_requests_total{{{labels}}} {val}")
        lines.append("# HELP llm_tokens_total Total tokens consumed.")
        lines.append("# TYPE llm_tokens_total counter")
        for labels, val in self.total_tokens.items():
            lines.append(f"llm_tokens_total{{{labels}}} {val}")
        return "\n".join(lines) + "\n"


registry = PrometheusRegistry()


@app.get("/metrics")
def get_metrics():
    body = registry.generate_prometheus_text()
    return Response(content=body, media_type="text/plain; version=0.0.4")


@app.get("/ask")
def ask():
    registry.inc_request("/ask", 200)
    registry.inc_tokens("gpt-4o", "prompt", 150)
    registry.inc_tokens("gpt-4o", "completion", 45)
    return {"reply": "Market quote"}


client = TestClient(app)
client.get("/ask")
metrics_resp = client.get("/metrics")

assert metrics_resp.status_code == 200
assert 'http_requests_total{endpoint="/ask",status="200"} 1' in metrics_resp.text
assert 'llm_tokens_total{model="gpt-4o",type="prompt"} 150' in metrics_resp.text
```

## Likely follow-ups

- Why should you avoid high-cardinality labels (like `user_id` or `session_id`) in Prometheus metrics?
- How does the Prometheus pull model compare with pushing metrics to StatsD/Datadog?

---

[← Q0857](../../batch_09_genai_services_fastapi/0857_opentelemetry_instrumentation_for_fastapi_routes_and/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0859 →](../../batch_09_genai_services_fastapi/0859_health_checks_deep_versus_shallow_liveness_and_readiness/README.md)
