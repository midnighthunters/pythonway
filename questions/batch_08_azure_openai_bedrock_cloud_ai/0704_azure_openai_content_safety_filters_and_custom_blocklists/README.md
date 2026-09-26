# Q0704 · Azure OpenAI content safety filters and custom blocklists

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

How does Azure OpenAI Content Safety protect applications from harmful content? Write Python code that inspects safety moderation scores and applies a bank compliance block.

## Answer

Azure OpenAI integrates multi-category content filtering that evaluates both user input prompts and model completion outputs against four harm categories: Hate, Sexual, Violence, and Self-Harm.

Severity levels are categorized as: `Safe` (0), `Low` (2), `Medium` (4), and `High` (6). Enterprise banks often set strict thresholds (blocking `Medium` and `High`) and configure custom blocklists for restricted financial terminology (e.g. proprietary trading strategy code names).

```python
from typing import Any, Dict, List


class AzureContentSafetyGuard:
    def __init__(self, block_threshold: int = 4, custom_blocklist: List[str] = None):
        self.block_threshold = block_threshold
        self.custom_blocklist = [w.lower() for w in (custom_blocklist or [])]

    def evaluate_content(self, text: str, safety_annotations: Dict[str, int]) -> Dict[str, Any]:
        # Check custom restricted terms
        text_lower = text.lower()
        for term in self.custom_blocklist:
            if term in text_lower:
                return {"allowed": False, "reason": f"Custom blocklist term detected: '{term}'"}

        # Check Azure severity scores (0=safe, 2=low, 4=medium, 6=high)
        for category, score in safety_annotations.items():
            if score >= self.block_threshold:
                return {"allowed": False, "reason": f"Azure safety violation in category '{category}' (score={score})"}

        return {"allowed": True, "reason": "Passed safety checks"}


guard = AzureContentSafetyGuard(block_threshold=4, custom_blocklist=["ProjectAegisAlpha"])

# Permitted prompt
ok_res = guard.evaluate_content("Summarize annual FX volume", {"hate": 0, "violence": 0, "self_harm": 0})
assert ok_res["allowed"] is True

# Blocked by Azure Content Safety threshold
unsafe_res = guard.evaluate_content("Harmful text", {"hate": 6, "violence": 2})
assert unsafe_res["allowed"] is False
assert "hate" in unsafe_res["reason"]

# Blocked by custom blocklist
custom_res = guard.evaluate_content("Status of ProjectAegisAlpha trades", {"hate": 0})
assert custom_res["allowed"] is False
assert "projectaegisalpha" in custom_res["reason"]
```

## Likely follow-ups

- What is the difference between synchronous content filtering and asynchronous moderation?
- How can a bank apply for modified content filtering to avoid false positives on legitimate financial crime analysis?

---

[← Q0703](../../batch_08_azure_openai_bedrock_cloud_ai/0703_azure_entra_id_and_managed_identity_authentication/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0705 →](../../batch_08_azure_openai_bedrock_cloud_ai/0705_private_endpoints_and_network_isolation_in_azure_openai/README.md)
