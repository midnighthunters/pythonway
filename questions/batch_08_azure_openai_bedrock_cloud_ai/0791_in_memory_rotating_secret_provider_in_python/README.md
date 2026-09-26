# Q0791 · In-memory rotating secret provider in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Multi-Cloud AI Gateways | Medium |

## Question

Write Python code implementing an in-memory rotating credential provider with thread-safe atomic credential swapping.

## Answer

```python
import threading
from typing import Any, Dict


class RotatingCredentialProvider:
    def __init__(self, initial_key: str):
        self._lock = threading.Lock()
        self._current_key = initial_key
        self._version = 1

    def get_active_credentials(self) -> Dict[str, Any]:
        with self._lock:
            return {"key": self._current_key, "version": self._version}

    def rotate_key(self, new_key: str) -> None:
        with self._lock:
            self._current_key = new_key
            self._version += 1


provider = RotatingCredentialProvider("sk-live-v1-initial-secret")
creds = provider.get_active_credentials()
assert creds["key"] == "sk-live-v1-initial-secret"
assert creds["version"] == 1

# Background rotation
provider.rotate_key("sk-live-v2-rotated-secret")
new_creds = provider.get_active_credentials()
assert new_creds["key"] == "sk-live-v2-rotated-secret"
assert new_creds["version"] == 2
```

## Likely follow-ups

- How does this pattern support blue-green deployments of model configurations?
- How can failed rotations trigger an automatic rollback to the previous working key?

---

[← Q0790](../../batch_08_azure_openai_bedrock_cloud_ai/0790_key_rotation_and_credential_reloading_without_service/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0792 →](../../batch_08_azure_openai_bedrock_cloud_ai/0792_canary_traffic_splitter_for_model_a_b_testing_in_python/README.md)
