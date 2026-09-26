# Q0962 · Redacting PII before public cloud LLM calls (Zero-Data Retention)

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Easy |

## Question

Write Python code implementing an outbound request interceptor that redacts customer email addresses and phone numbers before dispatching the payload to a public cloud LLM API.

## Answer

Under enterprise banking policy, all outbound requests to third-party or public cloud AI providers must pass through an outbound sanitation gateway that strips direct customer contact details.

```python
import re
from typing import Tuple


def redact_outbound_payload(prompt: str) -> Tuple[str, int]:
    # Patterns for email and phone numbers
    email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    phone_regex = re.compile(r"\b(?:\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b")

    redacted, count1 = email_regex.subn("[REDACTED_EMAIL]", prompt)
    redacted, count2 = phone_regex.subn("[REDACTED_PHONE]", redacted)
    return redacted, count1 + count2


raw = "Send investment memo to client at alice@investor.com or call 212-555-0199."
clean, total_redacted = redact_outbound_payload(raw)

assert total_redacted == 2
assert "alice@investor.com" not in clean
assert "212-555-0199" not in clean
assert "[REDACTED_EMAIL]" in clean
assert "[REDACTED_PHONE]" in clean
```

## Likely follow-ups

- Why is client-side redaction necessary even if the cloud provider signs a Business Associate Agreement (BAA)?
- How do you maintain conversational context when pronouns refer to redacted entities?

---

[← Q0961](../../batch_10_ai_security_responsible_ai/0961_customer_banking_secrecy_regulations_glba_gdpr_art_9_nydfs/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0963 →](../../batch_10_ai_security_responsible_ai/0963_differential_privacy_in_fine_tuning_and_synthetic_dataset/README.md)
