# Q0176 · Style guide compliance

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Output validation | Easy |

## Question

Corporate communications must follow a style guide (British spelling, no jargon, short sentences). Write a lint for generated text that flags banned phrases, American spellings and overlong sentences.

## Answer

```python
import re

BANNED = {"leverage": "use", "utilize": "use", "synergy": None, "going forward": "from now on"}
US_TO_UK = {"color": "colour", "organization": "organisation", "prioritize": "prioritise", "center": "centre"}


def style_lint(text: str, max_words: int = 30) -> list[str]:
    issues, low = [], text.lower()
    for phrase, alt in BANNED.items():
        if re.search(rf"\b{re.escape(phrase)}\b", low):
            issues.append(f"avoid '{phrase}'" + (f", use '{alt}'" if alt else ""))
    for us, uk in US_TO_UK.items():
        if re.search(rf"\b{us}\b", low):
            issues.append(f"use British spelling '{uk}'")
    for s in re.split(r"(?<=[.!?])\s+", text.strip()):
        if len(s.split()) > max_words:
            issues.append(f"sentence over {max_words} words: {s[:30]}...")
    return issues


assert style_lint("We will prioritise the colour scheme.") == []
issues = style_lint("Going forward we leverage synergy to prioritize the center. " + "word " * 31 + ".")
assert issues[:3] == ["avoid 'leverage', use 'use'", "avoid 'synergy'", "avoid 'going forward', use 'from now on'"]
assert "use British spelling 'prioritise'" in issues and any("sentence over" in i for i in issues)
```

Use the lint to trigger a targeted revision prompt ("fix these issues: …") rather than rejecting outright. Put the style guide's key rules into the prompt too, but the deterministic check is what guarantees compliance.

## Likely follow-ups

- Which style rules are better enforced by an LLM judge than by regex?

---

[← Q0175](../../batch_02_prompting_context_structured_output/0175_slot_filling_for_a_booking_assistant/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0177 →](../../batch_02_prompting_context_structured_output/0177_prompt_compression/README.md)
