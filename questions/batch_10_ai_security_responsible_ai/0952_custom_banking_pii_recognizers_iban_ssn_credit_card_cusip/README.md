# Q0952 · Custom banking PII recognizers: IBAN, SSN, Credit Card, CUSIP, Swift BIC

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Hard |

## Question

Write Python code implementing custom financial entity recognizers for International Bank Account Numbers (IBAN) with Mod-97 checksum validation and SWIFT/BIC codes.

## Answer

Standard PII libraries lack specialized banking identifier validation. An invalid 9-digit string should not trigger a false-positive IBAN alert, whereas a real IBAN must pass strict ISO 7064 Mod-97 checksum validation.

```python
import re


def validate_iban(iban: str) -> bool:
    """Validates an IBAN using ISO 7064 Mod-97 checksum algorithm."""
    clean_iban = iban.replace(" ", "").upper()
    if not re.match(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]{4,30}$", clean_iban):
        return False

    # Move first 4 characters to the end
    rearranged = clean_iban[4:] + clean_iban[:4]

    # Convert letters to digits (A=10, B=11, ..., Z=35)
    numeric_str = "".join(str(ord(c) - 55) if c.isalpha() else c for c in rearranged)

    # Perform integer modulo 97
    return int(numeric_str) % 97 == 1


def is_valid_swift_bic(bic: str) -> bool:
    """Validates 8 or 11 character ISO 9362 SWIFT/BIC code."""
    clean_bic = bic.replace(" ", "").upper()
    return bool(re.match(r"^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$", clean_bic))


# Valid UK test IBAN (Mod-97 == 1)
test_iban = "GB82 WEST 1234 5698 7654 32"
assert validate_iban(test_iban) is True

# Invalid IBAN
bad_iban = "GB82 WEST 1234 5698 7654 39"
assert validate_iban(bad_iban) is False

# SWIFT/BIC codes
assert is_valid_swift_bic("CHASUS33") is True
assert is_valid_swift_bic("CHASUS33XXX") is True
assert is_valid_swift_bic("INVALID_BIC") is False
```

## Likely follow-ups

- What is CUSIP / SEDOL / ISIN validation, and why are security identifiers considered confidential in trading contexts?
- How does Mod-97 math avoid floating-point overflow for 34-character numbers in Python?

---

[← Q0951](../../batch_10_ai_security_responsible_ai/0951_microsoft_presidio_architecture_analyzers_recognizers_and/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0953 →](../../batch_10_ai_security_responsible_ai/0953_reversible_pii_tokenization_pseudonymization_with_secure/README.md)
