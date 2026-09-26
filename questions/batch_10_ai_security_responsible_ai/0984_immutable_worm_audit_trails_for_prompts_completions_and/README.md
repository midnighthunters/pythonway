# Q0984 · Immutable WORM audit trails for prompts, completions, and tool calls

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Hard |

## Question

Explain Write-Once-Read-Many (WORM) storage requirements under SEC Rule 17a-4, and write Python code simulating an append-only cryptographic hash-chained audit log.

## Answer

Under SEC Rule 17a-4 and CFTC Rule 1.31, electronic records must be stored in Write-Once-Read-Many (WORM) format: records cannot be altered, overwritten, or erased during their retention period (typically 7 years).

A **cryptographic hash chain** links each log entry to the hash of the preceding entry. If an attacker modifies or deletes a historical record, all subsequent block hashes become invalid, exposing tampering.

```python
import hashlib
import json
import time
from typing import List, Dict, Any


class ImmutableLogBlock:
    def __init__(self, index: int, prev_hash: str, payload: Dict[str, Any], timestamp: float):
        self.index = index
        self.prev_hash = prev_hash
        self.payload = payload
        self.timestamp = timestamp
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        serialized = json.dumps(
            {"index": self.index, "prev_hash": self.prev_hash, "payload": self.payload, "ts": self.timestamp},
            sort_keys=True,
        )
        return hashlib.sha256(serialized.encode()).hexdigest()


class TamperEvidentAuditTrail:
    def __init__(self):
        genesis = ImmutableLogBlock(0, "0" * 64, {"event": "GENESIS"}, 0.0)
        self.chain: List[ImmutableLogBlock] = [genesis]

    def append_event(self, payload: Dict[str, Any]) -> str:
        prev = self.chain[-1]
        block = ImmutableLogBlock(len(self.chain), prev.hash, payload, time.time())
        self.chain.append(block)
        return block.hash

    def verify_chain_integrity(self) -> bool:
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            # Verify previous hash link
            if curr.prev_hash != prev.hash:
                return False
            # Verify current block's hash
            if curr.hash != curr.compute_hash():
                return False
        return True


audit = TamperEvidentAuditTrail()
h1 = audit.append_event({"user": "trader_1", "prompt": "Execute swap"})
h2 = audit.append_event({"user": "trader_2", "prompt": "Fetch curve"})

assert audit.verify_chain_integrity() is True

# Tampering simulation: attacker modifies block 1 payload
audit.chain[1].payload["prompt"] = "Execute malicious transfer"
assert audit.verify_chain_integrity() is False  # Tampering detected!
```

## Likely follow-ups

- How does AWS S3 Object Lock in Compliance Mode guarantee physical WORM immutability?
- What are the differences between Compliance Mode and Governance Mode in cloud storage?

---

[← Q0983](../../batch_10_ai_security_responsible_ai/0983_model_inventory_management_tiered_risk_rating_and_model/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0985 →](../../batch_10_ai_security_responsible_ai/0985_cryptographic_signing_of_llm_audit_logs_for_non_repudiation/README.md)
