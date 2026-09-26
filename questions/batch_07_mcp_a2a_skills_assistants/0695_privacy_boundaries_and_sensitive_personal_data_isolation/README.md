# Q0695 · Privacy boundaries and sensitive personal data isolation

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | Personal AI assistants | Medium |

## Question

Write Python code that checks personal assistant context for sensitive user PII (credit card numbers, social security numbers) and redacts them before passing context to an external LLM.

## Answer

```python
import re
from typing import Tuple


class PIIRedactor:
    SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
    CARD_PATTERN = re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")

    @classmethod
    def redact(cls, text: str) -> Tuple[str, int]:
        redactions = 0
        cleaned, n1 = cls.SSN_PATTERN.subn("[REDACTED_SSN]", text)
        redactions += n1
        cleaned, n2 = cls.CARD_PATTERN.subn("[REDACTED_CARD]", cleaned)
        redactions += n2
        return cleaned, redactions


raw_input = "User account SSN is 000-12-3456 and payment card is 4111-2222-3333-4444."
sanitized, count = PIIRedactor.redact(raw_input)

assert count == 2
assert "000-12-3456" not in sanitized
assert "4111-2222-3333-4444" not in sanitized
assert "[REDACTED_SSN]" in sanitized
assert "[REDACTED_CARD]" in sanitized
```

## Likely follow-ups

- Why is client-side PII scrubbing mandatory in regulated financial environments?
- What techniques restore redacted tokens when model responses return to the user?

---

[← Q0694](../../batch_07_mcp_a2a_skills_assistants/0694_cross_channel_personal_assistant_teams_slack_email_web/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0696 →](../../batch_07_mcp_a2a_skills_assistants/0696_zero_trust_architecture_for_enterprise_mcp_and_a2a_networks/README.md)
