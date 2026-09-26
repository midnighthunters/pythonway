# Q0364 · Redact PII before logging

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Privacy | Medium |

## Question

Implement a redactor for logs and traces covering email addresses, UK phone numbers, payment card numbers (with a Luhn check to cut false positives), IBANs and UK sort code plus account number.

## Answer

```python
import re


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, d in enumerate(reversed(digits)):
        n = int(d)
        if i % 2:
            n = n * 2 - 9 if n > 4 else n * 2
        total += n
    return total % 10 == 0


PATTERNS = [
    ("EMAIL", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){3,7}(?:\s?[A-Z0-9]{1,4})?\b")),
    ("UK_ACCOUNT", re.compile(r"\b\d{2}-\d{2}-\d{2}\s+\d{8}\b")),
    ("PHONE", re.compile(r"(?<!\d)(?:\+44\s?7\d{3}|07\d{3})\s?\d{3}\s?\d{3}(?!\d)")),
]
CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")


def redact(text: str) -> str:
    def card(m: re.Match) -> str:
        digits = re.sub(r"\D", "", m.group(0))
        return "[CARD]" if 13 <= len(digits) <= 19 and luhn_ok(digits) else m.group(0)

    text = CARD.sub(card, text)
    for label, rx in PATTERNS:
        text = rx.sub(f"[{label}]", text)
    return text


msg = ("Contact jane.doe@example.com or 07700 900123. Card 4111 1111 1111 1111, not 1234 5678 9012 3456. "
       "IBAN GB29 NWBK 6016 1331 9268 19, account 60-16-13 31926819.")
out = redact(msg)
assert "[EMAIL]" in out and "[PHONE]" in out and "[CARD]" in out and "1234 5678 9012 3456" in out
assert "[IBAN]" in out and "[UK_ACCOUNT]" in out and "jane.doe" not in out
```

The Luhn check keeps random 16-digit reference numbers from being redacted as cards. Regex redaction is a baseline. Add NER-based detection (names, addresses) through a service such as Microsoft Presidio or cloud PII detectors, and test the redactor on labelled samples for both leaks and over-redaction.

## Likely follow-ups

- Why are names much harder to redact reliably than card numbers?

---

[← Q0363](../../batch_04_llm_evaluation_observability/0363_structured_json_logs_for_llm_calls/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0365 →](../../batch_04_llm_evaluation_observability/0365_sample_traces_for_review/README.md)
