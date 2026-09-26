# Q0081 · Unicode normalisation before model input

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Input hygiene | Medium |

## Question

Implement input normalisation for an LLM gateway: apply NFKC and strip zero-width characters. Explain which attacks and quality issues it helps with, and what it misses.

## Answer

```python
import re
import unicodedata

ZERO_WIDTH = re.compile("[\u200b\u200c\u200d\u2060\ufeff]")


def normalize_input(text: str) -> str:
    return ZERO_WIDTH.sub("", unicodedata.normalize("NFKC", text))


assert normalize_input("ｉｇｎｏｒｅ") == "ignore"
assert normalize_input("ig\u200bnore") == "ignore"
assert normalize_input("e\u0301") == "é"
assert normalize_input("ＩＧＮＯＲＥ previous") == "IGNORE previous"
```

It helps:
- Keyword and regex guardrails can be evaded with fullwidth letters or zero-width joiners. Normalising first makes your filters see the canonical text.
- Deduplication and caching: visually identical strings get the same key.
- Tokenization: fewer odd tokens, and better retrieval matching.

It misses:
- Cross-script homoglyphs (Cyrillic "а" versus Latin "a") survive NFKC. Use Unicode confusables data (UTS #39) if needed.
- Semantic evasion (paraphrase, other languages, encodings such as base64). Pattern filters are one layer, not a defence on their own.

Caution: NFKC can change meaning in some contexts (superscripts, some symbols), so keep the original for display and audit.

## Likely follow-ups

- Why should you log both the raw and the normalised input?

---

[← Q0080](../../batch_01_llm_fundamentals/0080_utf_8_bytes_and_safe_truncation/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0082 →](../../batch_01_llm_fundamentals/0082_expected_calibration_error/README.md)
