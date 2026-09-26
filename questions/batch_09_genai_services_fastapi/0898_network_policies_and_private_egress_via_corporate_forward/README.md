# Q0898 · Network policies and private egress via corporate forward proxies

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Medium |

## Question

Explain how Kubernetes NetworkPolicies and corporate forward proxies (e.g. Squid, BlueCoat) enforce perimeter security for outbound LLM API requests, and configure HTTP client proxy routing in Python.

## Answer

In regulated banks, containers must **never** have unrestricted direct access to the public Internet.
1. **Kubernetes NetworkPolicy**: Restricts pod egress traffic so it can *only* connect to internal corporate forward proxies.
2. **Forward Proxy Inspection**: The proxy performs SSL inspection, verifies domain whitelists (e.g. `*.openai.azure.com`, `bedrock.*.amazonaws.com`), and blocks all unapproved egress.

```python
from typing import Dict


def configure_http_proxy_settings(is_corporate_env: bool) -> Dict[str, str]:
    if is_corporate_env:
        return {
            "http_proxy": "http://forward-proxy.jpmc.internal:8080",
            "https_proxy": "http://forward-proxy.jpmc.internal:8080",
            "no_proxy": "localhost,127.0.0.1,.internal,.svc.cluster.local",
        }
    return {}


proxies = configure_http_proxy_settings(is_corporate_env=True)
assert "https_proxy" in proxies
assert "forward-proxy.jpmc.internal" in proxies["https_proxy"]
assert ".svc.cluster.local" in proxies["no_proxy"]
```

## Likely follow-ups

- How do you install corporate Root CA certificates into container trust stores (`ca-certificates`)?
- What is the performance impact of forward proxy SSL interception on SSE streaming connections?

---

[← Q0897](../../batch_09_genai_services_fastapi/0897_optimizing_container_startup_time_for_serverless_containers/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0899 →](../../batch_09_genai_services_fastapi/0899_disaster_recovery_multi_region_active_passive_failover_and/README.md)
