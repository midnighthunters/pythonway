# Q0897 · Optimizing container startup time for serverless containers

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Easy |

## Question

Write Python code measuring module import times and lazy-loading heavy libraries (e.g. PyTorch, Pandas, LangChain) to optimize container cold starts.

## Answer

In serverless container environments (AWS Fargate, Azure Container Apps), cold start latency is dominated by Python imports: `import torch` can take 2-4 seconds. Lazy loading delays imports until the first route invocation requiring them.

```python
import time


class LazyModuleLoader:
    def __init__(self):
        self._module = None

    def get_module(self):
        if self._module is None:
            # Simulated heavy import
            time.sleep(0.01)
            self._module = {"loaded": True, "version": "2.4.0"}
        return self._module


loader = LazyModuleLoader()
# Startup is instantaneous: heavy module not imported yet
assert loader._module is None

# Imported on first route call
mod = loader.get_module()
assert mod["loaded"] is True
assert loader._module is not None
```

## Likely follow-ups

- How does Python 3.12+ improve startup speed compared to earlier Python versions?
- How do container image layer caching and eStargz (lazy pulling) accelerate container startup?

---

[← Q0896](../../batch_09_genai_services_fastapi/0896_container_security_scanning_and_minimal_base_images/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0898 →](../../batch_09_genai_services_fastapi/0898_network_policies_and_private_egress_via_corporate_forward/README.md)
