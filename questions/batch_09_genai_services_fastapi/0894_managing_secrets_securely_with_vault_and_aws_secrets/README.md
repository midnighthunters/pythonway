# Q0894 · Managing secrets securely with Vault and AWS Secrets Manager in containers

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Easy |

## Question

Write Python code demonstrating secure secret injection via environment variables or volume-mounted files, validating that API keys are never printed in logs or error messages.

## Answer

Hardcoding cloud credentials (Azure OpenAI keys, AWS secret keys) in container images or source code breaches security policies. Secrets should be mounted into `/mnt/secrets/` as ephemeral RAM volumes or injected via Kubernetes Secrets backed by HashiCorp Vault.

```python
import os
from typing import Optional


class SecretLoader:
    @staticmethod
    def load_secret(env_var_name: str, file_path: Optional[str] = None) -> str:
        # Priority 1: Mounted Vault file
        if file_path and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        # Priority 2: Injected Environment variable
        val = os.getenv(env_var_name)
        if not val:
            raise ValueError(f"Required secret {env_var_name} not found")
        return val

    @staticmethod
    def mask_secret(secret_val: str) -> str:
        '''Returns safe masked string for telemetry logs.'''
        if len(secret_val) <= 6:
            return "***"
        return f"{secret_val[:3]}...{secret_val[-3:]}"


os.environ["AZURE_OPENAI_API_KEY"] = "sk-jpmc-live-secret-key-998822"

key = SecretLoader.load_secret("AZURE_OPENAI_API_KEY")
assert key.startswith("sk-jpmc")

masked = SecretLoader.mask_secret(key)
assert masked == "sk-...822"
assert "secret-key" not in masked
```

## Likely follow-ups

- What is the security advantage of volume-mounted secret files over environment variables?
- How does HashiCorp Vault Agent sidecar rotate secrets without restarting container pods?

---

[← Q0893](../../batch_09_genai_services_fastapi/0893_rolling_zero_downtime_deployments_and_blue_green_canary/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0895 →](../../batch_09_genai_services_fastapi/0895_ephemeral_volume_mounts_and_ram_disks_for_temporary_file/README.md)
