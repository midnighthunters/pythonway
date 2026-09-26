# Q0928 · OWASP LLM03: Supply Chain Vulnerabilities in model hubs and LoRA adapters

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | OWASP LLM Top 10 | Medium |

## Question

Explain OWASP LLM03: Supply Chain Vulnerabilities in AI pipelines, and write Python code verifying cryptographic SHA-256 hashes of model weights before loading.

## Answer

AI supply chain vulnerabilities arise from downloading unvetted models, tokenizers, or LoRA adapters from public hubs (HuggingFace, GitHub). Attackers can upload backdoored weights, poisoned fine-tuning datasets, or pickled model files containing arbitrary code execution payloads (`torch.load()` on untrusted pickle files).

Enterprise standards require:
1. Using `safetensors` format instead of Python pickle files.
2. Cryptographically verifying SHA-256 hashes against approved internal model inventories.

```python
import hashlib
import io


def verify_model_weights_hash(weight_stream: io.BytesIO, expected_sha256: str) -> bool:
    sha = hashlib.sha256()
    while chunk := weight_stream.read(4096):
        sha.update(chunk)
    calculated_hash = sha.hexdigest()
    return calculated_hash.lower() == expected_sha256.lower()


# Simulation of vetted model weight file
fake_weights = b"SAFETENSORS_HEADER_WEIGHTS_DATA_V1"
expected = hashlib.sha256(fake_weights).hexdigest()

stream_valid = io.BytesIO(fake_weights)
assert verify_model_weights_hash(stream_valid, expected) is True

# Tampered weights
stream_tampered = io.BytesIO(fake_weights + b"_TAMPERED")
assert verify_model_weights_hash(stream_tampered, expected) is False
```

## Likely follow-ups

- Why is `torch.load()` dangerous when run on untrusted `.bin` or `.pt` model files?
- How does an enterprise Model Registry (like MLflow or Artifactory) enforce provenance?

---

[← Q0927](../../batch_10_ai_security_responsible_ai/0927_owasp_llm02_sensitive_information_disclosure_and_model/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0929 →](../../batch_10_ai_security_responsible_ai/0929_owasp_llm04_data_and_model_poisoning_in_fine_tuning_and_pre/README.md)
