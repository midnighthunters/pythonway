# Q0938 · Step-up authentication and TOTP verification in agent workflows

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Agent security | Easy |

## Question

Write Python code implementing Time-based One-Time Password (TOTP) verification for step-up authentication when an agent initiates a sensitive financial transaction.

## Answer

When a user asks an agent to perform a high-risk operation (e.g., "Change wire transfer limit to $1M"), the agent must demand step-up authentication (MFA/TOTP) before executing the tool.

```python
import hmac
import hashlib
import struct
import time


def generate_mock_totp(secret: bytes, time_step: int = 30) -> str:
    counter = int(time.time() // time_step)
    msg = struct.pack(">Q", counter)
    h = hmac.new(secret, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code = (struct.unpack(">I", h[offset : offset + 4])[0] & 0x7FFFFFFF) % 1_000_000
    return f"{code:06d}"


def verify_totp(user_provided_code: str, secret: bytes) -> bool:
    current_code = generate_mock_totp(secret)
    # Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(user_provided_code, current_code)


shared_secret = b"JPMC_MFA_SECRET_KEY_12345"
valid_code = generate_mock_totp(shared_secret)

assert verify_totp(valid_code, shared_secret) is True
assert verify_totp("000000", shared_secret) is False
```

## Likely follow-ups

- Why is `hmac.compare_digest()` essential when comparing cryptographic tokens?
- How does FIDO2 / WebAuthn hardware key authentication compare with TOTP for agent security?

---

[← Q0937](../../batch_10_ai_security_responsible_ai/0937_human_in_the_loop_approval_gates_for_sensitive_bank_actions/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0939 →](../../batch_10_ai_security_responsible_ai/0939_agent_impersonation_and_synthetic_identity_spoofing/README.md)
