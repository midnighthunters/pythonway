# Q0792 · Canary traffic splitter for model A/B testing in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

Write Python code implementing a hash-based deterministic canary traffic splitter that routes a percentage of user requests to a candidate model based on user ID.

## Answer

Deterministic hashing ensures that a specific user experiences a consistent model across multi-turn sessions rather than flipping randomly between Model A and Model B on each turn.

```python
import hashlib


class CanaryTrafficSplitter:
    def __init__(self, canary_percentage: int = 20):
        self.canary_percentage = canary_percentage  # 0 to 100

    def select_model(self, user_id: str, baseline_model: str, candidate_model: str) -> str:
        # Compute deterministic hash of user_id (0 to 99)
        digest = hashlib.md5(user_id.encode("utf-8")).hexdigest()
        bucket = int(digest[:4], 16) % 100

        if bucket < self.canary_percentage:
            return candidate_model
        return baseline_model


splitter = CanaryTrafficSplitter(canary_percentage=25)

# Same user always gets the same model assignment across multiple calls
m1 = splitter.select_model("user_alice@jpmc.com", "gpt-4o-baseline", "gpt-4o-candidate")
m2 = splitter.select_model("user_alice@jpmc.com", "gpt-4o-baseline", "gpt-4o-candidate")
assert m1 == m2

# Test distribution across 100 simulated users
assignments = [splitter.select_model(f"user_{i}", "baseline", "candidate") for i in range(100)]
candidate_count = assignments.count("candidate")
assert 15 <= candidate_count <= 35  # Approximate 25% distribution
```

## Likely follow-ups

- Why is hashing on `user_id` preferable to random `random.random() < 0.25` for A/B testing?
- How do you handle multi-agent handoffs when different agents might select different model versions?

---

[← Q0791](../../batch_08_azure_openai_bedrock_cloud_ai/0791_in_memory_rotating_secret_provider_in_python/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0793 →](../../batch_08_azure_openai_bedrock_cloud_ai/0793_error_classification_transient_vs_terminal_cloud_ai_errors/README.md)
