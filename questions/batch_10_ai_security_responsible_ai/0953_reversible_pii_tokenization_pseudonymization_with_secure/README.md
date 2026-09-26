# Q0953 · Reversible PII tokenization (pseudonymization) with secure lookup mapping

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Medium |

## Question

Write Python code implementing reversible PII pseudonymization, replacing sensitive names and account numbers with synthetic surrogate tokens before calling cloud LLMs, and restoring original values in the output.

## Answer

Financial institutions often utilize public cloud LLM endpoints (Azure OpenAI, AWS Bedrock) under zero-data retention agreements. To ensure zero PII leaves the corporate perimeter:
1. Customer names and account numbers are replaced with reversible surrogate tokens (`CUSTOMER_1`, `ACCOUNT_1`).
2. The LLM reasons over the anonymized text.
3. The response is de-anonymized inside the bank firewall before reaching the user.

```python
import re
from typing import Dict, Tuple


class ReversiblePIITokenizer:
    def __init__(self):
        self.name_map: Dict[str, str] = {}
        self.reverse_map: Dict[str, str] = {}
        self.counter = 0

    def tokenize(self, text: str, sensitive_entities: list[str]) -> str:
        tokenized_text = text
        for ent in sensitive_entities:
            if ent not in self.name_map:
                self.counter += 1
                token = f"TOKEN_ENTITY_{self.counter}"
                self.name_map[ent] = token
                self.reverse_map[token] = ent

            tokenized_text = re.sub(re.escape(ent), self.name_map[ent], tokenized_text)
        return tokenized_text

    def detokenize(self, model_response: str) -> str:
        detokenized = model_response
        for token, original in self.reverse_map.items():
            detokenized = detokenized.replace(token, original)
        return detokenized


tokenizer = ReversiblePIITokenizer()

original_prompt = "Transfer $50,000 from client John Smith to client Alice Walker."
sanitized_prompt = tokenizer.tokenize(original_prompt, ["John Smith", "Alice Walker"])

assert "John Smith" not in sanitized_prompt
assert "Alice Walker" not in sanitized_prompt
assert "TOKEN_ENTITY_1" in sanitized_prompt
assert "TOKEN_ENTITY_2" in sanitized_prompt

# Simulated model response referencing the tokens
mock_model_reply = "Confirmed transfer of $50,000 from TOKEN_ENTITY_1 to TOKEN_ENTITY_2."
restored_reply = tokenizer.detokenize(mock_model_reply)

assert restored_reply == "Confirmed transfer of $50,000 from John Smith to Alice Walker."
```

## Likely follow-ups

- What encryption at rest standards (AES-GCM-256) must protect the surrogate mapping table?
- What happens if the LLM hallucinating variations of the token string (e.g. `TOKEN_ENTITY_1_A`) breaks de-tokenization?

---

[← Q0952](../../batch_10_ai_security_responsible_ai/0952_custom_banking_pii_recognizers_iban_ssn_credit_card_cusip/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0954 →](../../batch_10_ai_security_responsible_ai/0954_irreversible_pii_masking_redaction_and_synthetic_data/README.md)
