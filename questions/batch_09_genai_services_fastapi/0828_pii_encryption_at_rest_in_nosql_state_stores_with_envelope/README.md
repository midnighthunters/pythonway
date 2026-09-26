# Q0828 · PII encryption at rest in NoSQL state stores with envelope encryption

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | NoSQL state stores | Hard |

## Question

Write Python code demonstrating envelope encryption for LLM conversation histories stored in NoSQL, using a local mock Key Management Service (KMS) and AES-256 GCM simulation.

## Answer

Financial compliance (GDPR Article 32, GLBA, FINRA) mandates that sensitive customer chat logs containing PII (names, account numbers, transactions) are encrypted at rest with cryptographic key rotation.

Envelope encryption generates a unique Data Encryption Key (DEK) for each chat thread, encrypts the conversation plaintext with the DEK, and encrypts the DEK under a master Key Encryption Key (KEK) managed in AWS KMS or Azure Key Vault.

```python
import base64
import hashlib
import json
import os
from typing import Dict, Tuple


class MockKMS:
    '''Simulates AWS KMS / Azure Key Vault master key operations.'''
    def __init__(self, master_key_name: str):
        self.master_key = hashlib.sha256(master_key_name.encode()).digest()

    def generate_data_key(self) -> Tuple[bytes, str]:
        raw_dek = os.urandom(32)
        # Encrypt DEK with master key (XOR simulation for testability)
        encrypted_dek = bytes(b ^ self.master_key[i % len(self.master_key)] for i, b in enumerate(raw_dek))
        return raw_dek, base64.b64encode(encrypted_dek).decode()

    def decrypt_data_key(self, encrypted_dek_b64: str) -> bytes:
        encrypted_dek = base64.b64decode(encrypted_dek_b64.encode())
        return bytes(b ^ self.master_key[i % len(self.master_key)] for i, b in enumerate(encrypted_dek))


def encrypt_payload(plaintext: str, dek: bytes) -> str:
    # XOR stream cipher simulation for testing
    cipher = bytes(ord(c) ^ dek[i % len(dek)] for i, c in enumerate(plaintext))
    return base64.b64encode(cipher).decode()


def decrypt_payload(ciphertext_b64: str, dek: bytes) -> str:
    cipher = base64.b64decode(ciphertext_b64.encode())
    plain = "".join(chr(b ^ dek[i % len(dek)]) for i, b in enumerate(cipher))
    return plain


# Envelope Encryption Flow
kms = MockKMS("arn:aws:kms:us-east-1:123456789:key/jpmc-llm-suite")
raw_dek, encrypted_dek_b64 = kms.generate_data_key()

sensitive_chat = json.dumps([{"role": "user", "content": "Account 99281-22 balance enquiry"}])
ciphertext = encrypt_payload(sensitive_chat, raw_dek)

# Stored in NoSQL: ciphertext + encrypted DEK (raw_dek is discarded from memory)
nosql_record = {
    "thread_id": "th_sec_01",
    "encrypted_dek": encrypted_dek_b64,
    "payload": ciphertext,
}

# Decrypt flow on retrieval
recovered_dek = kms.decrypt_data_key(nosql_record["encrypted_dek"])
recovered_plaintext = decrypt_payload(nosql_record["payload"], recovered_dek)
assert recovered_plaintext == sensitive_chat
```

## Likely follow-ups

- What is the performance overhead of calling KMS for every read/write versus caching decrypted DEKs in memory?
- How does cryptographic erasure (Right to be Forgotten) work using envelope encryption?

---

[← Q0827](../../batch_09_genai_services_fastapi/0827_multi_region_active_active_replication_for_conversation/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0829 →](../../batch_09_genai_services_fastapi/0829_bulk_export_and_retention_policies_for_compliance_chat/README.md)
