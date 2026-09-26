# Q0799 · Cryptographic audit batch signer in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Cloud AI Compliance | Medium |

## Question

Write Python code that packages a batch of LLM invocation audit records into a canonical JSON payload, calculates an HMAC-SHA256 signature, and verifies data integrity.

## Answer

```python
import hashlib
import hmac
import json
from typing import Any, Dict, List


class AuditBatchSigner:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode("utf-8")

    def sign_batch(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Canonical sort for deterministic serialization
        payload_str = json.dumps(records, sort_keys=True)
        signature = hmac.new(self.secret_key, payload_str.encode("utf-8"), hashlib.sha256).hexdigest()
        return {
            "record_count": len(records),
            "payload": records,
            "signature_sha256": signature,
        }

    def verify_batch(self, batch_obj: Dict[str, Any]) -> bool:
        records = batch_obj["payload"]
        sig = batch_obj["signature_sha256"]
        expected_sig = hmac.new(
            self.secret_key, json.dumps(records, sort_keys=True).encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(sig, expected_sig)


signer = AuditBatchSigner("enterprise-audit-secret-2026")
batch = [
    {"user": "trader_1", "model": "gpt-4o", "trade_id": "TRD-100", "status": "approved"},
    {"user": "trader_2", "model": "claude-3-5", "trade_id": "TRD-101", "status": "flagged"},
]

signed_batch = signer.sign_batch(batch)
assert signer.verify_batch(signed_batch) is True

# Tampering attempt
signed_batch["payload"][0]["status"] = "tampered"
assert signer.verify_batch(signed_batch) is False
```

## Likely follow-ups

- Why is canonical JSON sorting mandatory before cryptographic signing?
- How do public-key asymmetric signatures (RSA / ECDSA) differ from symmetric HMAC in regulatory audits?

---

[← Q0798](../../batch_08_azure_openai_bedrock_cloud_ai/0798_audit_trail_persistence_to_immutable_storage/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0800 →](../../batch_08_azure_openai_bedrock_cloud_ai/0800_comprehensive_end_to_end_integration_test_of_a_multi_cloud/README.md)
