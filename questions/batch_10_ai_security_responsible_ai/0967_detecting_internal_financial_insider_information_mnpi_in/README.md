# Q0967 · Detecting internal financial insider information (MNPI) in prompts

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Hard |

## Question

Explain Material Non-Public Information (MNPI) under SEC Rule 10b-5, and write Python code implementing an automated MNPI keyword and project codename interceptor.

## Answer

Trading or communicating Material Non-Public Information (MNPI) regarding impending mergers, acquisitions, regulatory actions, or unannounced earnings violates SEC Rule 10b-5 and leads to criminal prosecution.

Employees interacting with GenAI tools must be prevented from pasting MNPI project codenames (e.g. "Project Apollo", "Target X M&A") into public or shared internal LLMs.

```python
import re
from typing import List, Tuple


class MNPIInterceptionFilter:
    def __init__(self, restricted_codenames: List[str]):
        # Build regex matching confidential project codenames
        escaped = [re.escape(name) for name in restricted_codenames]
        pattern_str = r"\b(" + "|".join(escaped) + r")\b"
        self.codename_regex = re.compile(pattern_str, re.IGNORECASE)

    def scan_for_mnpi(self, text: str) -> Tuple[bool, List[str]]:
        matches = self.codename_regex.findall(text)
        if matches:
            # Case-insensitive unique matches
            found = list(set(m.upper() for m in matches))
            return True, found
        return False, []


active_deals = ["PROJECT TITAN", "PROJECT FALCON", "ACQUISITION OMEGA"]
filter_engine = MNPIInterceptionFilter(active_deals)

safe_text = "What are the market implications of interest rate cuts?"
has_mnpi, items = filter_engine.scan_for_mnpi(safe_text)
assert has_mnpi is False

breach_text = "Draft an executive summary for Project Titan merger structure."
has_mnpi2, items2 = filter_engine.scan_for_mnpi(breach_text)
assert has_mnpi2 is True
assert "PROJECT TITAN" in items2
```

## Likely follow-ups

- What is an Ethical Wall (Chinese Wall) in an investment bank, and how does it restrict AI models?
- What regulatory reporting must occur when an employee pastes MNPI into an unapproved AI system?

---

[← Q0966](../../batch_10_ai_security_responsible_ai/0966_right_to_be_forgotten_gdpr_art_17_deleting_customer_data/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0968 →](../../batch_10_ai_security_responsible_ai/0968_watermarking_llm_outputs_for_forensic_provenance_and/README.md)
