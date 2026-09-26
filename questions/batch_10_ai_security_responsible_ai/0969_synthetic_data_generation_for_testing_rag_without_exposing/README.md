# Q0969 · Synthetic data generation for testing RAG without exposing customer PII

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Medium |

## Question

Write Python code using Faker-style template generation to create realistic, synthetic financial customer profiles for RAG testing without utilizing production customer PII.

## Answer

Testing RAG retrieval systems on production databases risks exposing customer financial transactions in staging environments. Generating synthetic, statistically realistic customer portfolios eliminates regulatory risk.

```python
import random
from typing import Dict, List


def generate_synthetic_customer_record(customer_id: int) -> Dict[str, str]:
    first_names = ["James", "Emma", "Liam", "Olivia", "Noah"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]
    cities = ["New York", "London", "Hong Kong", "Singapore", "Zurich"]

    # Deterministic generation based on customer_id
    rng = random.Random(customer_id)
    name = f"{rng.choice(first_names)} {rng.choice(last_names)}"
    balance = rng.randint(10_000, 5_000_000)
    city = rng.choice(cities)

    return {
        "customer_id": f"SYNTH_{customer_id:05d}",
        "full_name": name,
        "account_balance_usd": f"${balance:,.2f}",
        "branch_location": city,
        "is_synthetic": "TRUE",
    }


rec1 = generate_synthetic_customer_record(101)
rec2 = generate_synthetic_customer_record(102)

assert rec1["customer_id"] == "SYNTH_00101"
assert rec1["is_synthetic"] == "TRUE"
assert rec1["account_balance_usd"].startswith("$")
assert rec1["customer_id"] != rec2["customer_id"]
```

## Likely follow-ups

- How do generative tabular models (CTGAN, TVAE) generate privacy-preserving synthetic financial datasets?
- How do you validate that synthetic datasets maintain downstream statistical correlations?

---

[← Q0968](../../batch_10_ai_security_responsible_ai/0968_watermarking_llm_outputs_for_forensic_provenance_and/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0970 →](../../batch_10_ai_security_responsible_ai/0970_redacting_sensitive_connection_strings_and_secrets_from/README.md)
