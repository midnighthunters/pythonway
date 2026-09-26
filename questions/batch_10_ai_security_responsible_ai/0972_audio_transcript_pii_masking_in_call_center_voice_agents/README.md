# Q0972 · Audio transcript PII masking in call center voice agents

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Easy |

## Question

Write Python code implementing automated audio transcript PII masking for speech-to-text outputs in banking call center agent workflows.

## Answer

When customer calls are transcribed in real-time, callers state payment card numbers, dates of birth, and PINs. The streaming transcript pipeline must mask spoken numbers before displaying the transcript to customer service representatives or passing it to agent summarizers.

```python
import re


def mask_spoken_payment_card(transcript: str) -> str:
    # Pattern matching 16-digit sequences whether spoken continuously or grouped in 4s
    card_pattern = re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b")
    # Pattern matching spoken CVV/PIN
    cvv_pattern = re.compile(r"\b(?:security code|cvv|pin) (?:is )?(\d{3,4})\b", re.IGNORECASE)

    sanitized = card_pattern.sub("[CARD_NUMBER_MASKED]", transcript)
    sanitized = cvv_pattern.sub(r"security code [MASKED_CVV]", sanitized)
    return sanitized


call_snippet = "My card number is 4111 2222 3333 4444 and my security code is 882."
masked = mask_spoken_payment_card(call_snippet)

assert "4111 2222 3333 4444" not in masked
assert "882" not in masked
assert "[CARD_NUMBER_MASKED]" in masked
assert "[MASKED_CVV]" in masked
```

## Likely follow-ups

- How do PCI-DSS (Payment Card Industry Data Security Standard) rules govern audio recordings?
- How does audio bleeping (muting audio timestamps corresponding to PII words) work?

---

[← Q0971](../../batch_10_ai_security_responsible_ai/0971_optical_character_recognition_pii_scrubbing_from_uploaded/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0973 →](../../batch_10_ai_security_responsible_ai/0973_evaluating_pii_redaction_precision_recall_and_false/README.md)
