# Q0943 · Agent credential management: avoiding long-lived API tokens in agent memory

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Easy |

## Question

Why should long-lived API keys never be passed directly to an LLM agent, and write Python code demonstrating scoped ephemeral bearer token issuance.

## Answer

Passing master cloud API keys directly into LLM prompts or tool context risks catastrophic exposure if the model leaks its prompt context or logs are inspected.

Instead, agents should be issued short-lived, narrowly-scoped ephemeral credentials (e.g., AWS STS AssumeRole tokens or Azure Managed Identity OAuth2 tokens valid for 15 minutes).

```python
import time
import secrets
from typing import Dict


class EphemeralTokenIssuer:
    def __init__(self, token_validity_sec: int = 900):  # 15 minutes
        self.validity = token_validity_sec
        self.active_tokens: Dict[str, dict] = {}

    def issue_token(self, agent_id: str, allowed_scope: str) -> str:
        token = f"ephem_{secrets.token_hex(16)}"
        self.active_tokens[token] = {
            "agent_id": agent_id,
            "scope": allowed_scope,
            "expires_at": time.time() + self.validity,
        }
        return token

    def validate_token(self, token: str, required_scope: str) -> bool:
        record = self.active_tokens.get(token)
        if not record:
            return False
        if time.time() > record["expires_at"]:
            del self.active_tokens[token]
            return False
        return record["scope"] == required_scope


issuer = EphemeralTokenIssuer(token_validity_sec=10)
tok = issuer.issue_token("Agent_FX_Analyst", "read:market_data")

assert issuer.validate_token(tok, "read:market_data") is True
assert issuer.validate_token(tok, "write:trade_execution") is False

# Expire token
issuer.active_tokens[tok]["expires_at"] = time.time() - 1
assert issuer.validate_token(tok, "read:market_data") is False
```

## Likely follow-ups

- How does AWS IAM Roles for Service Accounts (IRSA) automate ephemeral token injection in Kubernetes?
- What is the difference between OAuth2 Bearer tokens and Proof-of-Possession (PoP) tokens?

---

[← Q0942](../../batch_10_ai_security_responsible_ai/0942_limiting_file_system_access_in_agent_tools/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0944 →](../../batch_10_ai_security_responsible_ai/0944_guarding_against_unauthorized_database_mutations_enforcing/README.md)
