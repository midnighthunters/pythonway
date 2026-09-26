# Q0985 · Cryptographic signing of LLM audit logs for non-repudiation

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Hard |

## Question

Write Python code implementing HMAC-SHA256 digital signing and verification of LLM completion audit events to ensure non-repudiation in legal disputes.

## Answer

If a customer claims an automated agent gave illegal financial advice, the bank must prove in court that the audit record is authentic and unaltered. Digitally signing every audit log record with an internal server key establishes non-repudiation.

```python
import hmac
import hashlib
import json
from typing import Dict, Tuple


class AuditRecordSigner:
    def __init__(self, signing_key: bytes):
        self.key = signing_key

    def sign_record(self, record: dict) -> Tuple[dict, str]:
        serialized = json.dumps(record, sort_keys=True)
        signature = hmac.new(self.key, serialized.encode(), hashlib.sha256).hexdigest()
        return record, signature

    def verify_signature(self, record: dict, signature: str) -> bool:
        serialized = json.dumps(record, sort_keys=True)
        expected = hmac.new(self.key, serialized.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected)


signer = AuditRecordSigner(b"jpmc-master-audit-hsm-key")
audit_entry = {
    "timestamp": "2026-09-26T10:00:00Z",
    "user_id": "cust_4821",
    "model": "gpt-4o",
    "prompt": "What are your treasury bond rates?",
    "completion": "Our current 10-year Treasury yield is 4.15%.",
}

rec, sig = signer.sign_record(audit_entry)
assert signer.verify_signature(rec, sig) is True

# Tampering with rate in completion
tampered = dict(rec)
tampered["completion"] = "Our current 10-year Treasury yield is 14.15%."
assert signer.verify_signature(tampered, sig) is False
```

## Likely follow-ups

- What is the difference between HMAC symmetric signatures and RSA/ECDSA asymmetric signatures?
- How do Hardware Security Modules (HSMs) protect private audit signing keys?

---

[← Q0984](../../batch_10_ai_security_responsible_ai/0984_immutable_worm_audit_trails_for_prompts_completions_and/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0986 →](../../batch_10_ai_security_responsible_ai/0986_automated_red_teaming_pipelines_for_continuous/README.md)
