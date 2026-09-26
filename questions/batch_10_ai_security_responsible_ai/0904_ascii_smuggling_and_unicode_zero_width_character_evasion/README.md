# Q0904 · ASCII smuggling and Unicode zero-width character evasion detection

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Prompt injection defense | Hard |

## Question

Explain ASCII smuggling and zero-width Unicode steganography in prompt injection, and write Python code detecting and stripping hidden Unicode characters from prompts.

## Answer

Attackers use Unicode zero-width characters (e.g. `\u200B` Zero-Width Space, `\u200C` Zero-Width Non-Joiner, `\u200D` Zero-Width Joiner) or Unicode tags (`\U000E0000` block) to hide instructions from human reviewers, firewalls, and regex filters. When decoded by tokenizers, these invisible characters reconstruct adversarial commands.

```python
import unicodedata
import re


def detect_and_clean_invisible_unicode(text: str) -> tuple[str, int]:
    # Regex matching zero-width spaces, joiners, directional overrides, and tag characters
    zero_width_pattern = re.compile(
        r"[\u200B-\u200D\uFEFF\u200E\u200F\u202A-\u202E\U000E0020-\U000E007F]"
    )
    matches = zero_width_pattern.findall(text)
    cleaned = zero_width_pattern.sub("", text)
    return cleaned, len(matches)


# Attack string: "Hello" with invisible zero-width characters embedded
smuggled = "What is\u200B\u200C the\u200D stock price?"
clean, count = detect_and_clean_invisible_unicode(smuggled)

assert count == 3
assert clean == "What is the stock price?"
assert "\u200B" not in clean
```

## Likely follow-ups

- How does ASCII smuggling encode binary payloads into Unicode tag characters?
- How does Unicode normalization (NFKC / NFD) help sanitize homoglyph attacks?

---

[← Q0903](../../batch_10_ai_security_responsible_ai/0903_delimiter_hijacking_and_instruction_boundary_isolation/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0905 →](../../batch_10_ai_security_responsible_ai/0905_base64_and_hex_encoding_evasion_in_user_prompts/README.md)
