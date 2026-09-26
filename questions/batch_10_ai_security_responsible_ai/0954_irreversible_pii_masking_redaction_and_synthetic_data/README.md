# Q0954 · Irreversible PII masking, redaction, and synthetic data replacement

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Easy |

## Question

Compare irreversible masking, full redaction, and synthetic data replacement, and write Python code implementing each method for US Social Security Numbers.

## Answer

| Technique | Output Format | Preserves Utility? | Reversible? |
|---|---|---|---|
| **Full Redaction** | `[REDACTED_SSN]` | No (loses structure) | No |
| **Masking** | `***-**-6789` | Partial (preserves last 4 digits for verification) | No |
| **Synthetic Replacement** | `000-12-3456` (fake valid format) | High (model understands it as an SSN without knowing real ID) | No (unless lookup stored) |

```python
import re


def redact_ssn(text: str) -> str:
    return re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", text)


def mask_ssn(text: str) -> str:
    # Retains only the last 4 digits
    return re.sub(r"\b\d{3}-\d{2}-(\d{4})\b", r"***-**-\1", text)


def synthetic_replace_ssn(text: str) -> str:
    return re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "000-00-0000", text)


sample = "Applicant SSN is 987-65-4321."
assert redact_ssn(sample) == "Applicant SSN is [REDACTED_SSN]."
assert mask_ssn(sample) == "Applicant SSN is ***-**-4321."
assert synthetic_replace_ssn(sample) == "Applicant SSN is 000-00-0000."
```

## Likely follow-ups

- Why does synthetic data replacement preserve downstream LLM reasoning better than full redaction?
- When does masking the last 4 digits breach banking privacy policies?

---

[← Q0953](../../batch_10_ai_security_responsible_ai/0953_reversible_pii_tokenization_pseudonymization_with_secure/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0955 →](../../batch_10_ai_security_responsible_ai/0955_handling_pii_in_unstructured_multi_turn_chat_dialogues/README.md)
