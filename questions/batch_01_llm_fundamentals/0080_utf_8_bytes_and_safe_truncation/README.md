# Q0080 · UTF-8 bytes and safe truncation

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Text handling | Medium |

## Question

Many limits are in bytes (headers, database columns, some API fields). Implement truncation of a string to a maximum number of UTF-8 bytes without splitting a character.

## Answer

UTF-8 uses 1–4 bytes per character, and continuation bytes match the bit pattern `10xxxxxx`. If the first excluded byte is a continuation byte, the character straddles the cut, so move the cut back to that character's lead byte.

```python
def safe_truncate_utf8(s: str, max_bytes: int) -> str:
    b = s.encode("utf-8")
    if len(b) <= max_bytes:
        return s
    cut = max_bytes
    while cut > 0 and (b[cut] & 0xC0) == 0x80:
        cut -= 1
    return b[:cut].decode("utf-8")


assert len("😀".encode()) == 4 and len("é".encode()) == 2
assert safe_truncate_utf8("héllo", 2) == "h"
assert safe_truncate_utf8("héllo", 3) == "hé"
assert safe_truncate_utf8("a😀b", 3) == "a"
assert safe_truncate_utf8("a😀b", 5) == "a😀"
assert safe_truncate_utf8("abc", 10) == "abc"
```

Byte-level BPE tokenizers work on these bytes, which is why a single emoji or CJK character can cost several tokens, and why decoding a partial token stream can produce invalid UTF-8 mid-stream. Streaming clients must buffer incomplete byte sequences.

## Likely follow-ups

- Grapheme clusters (emoji with skin-tone modifiers, flags) can be several code points. How would you avoid splitting those?

---

[← Q0079](../../batch_01_llm_fundamentals/0079_bigram_language_model_with_smoothing/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0081 →](../../batch_01_llm_fundamentals/0081_unicode_normalisation_before_model_input/README.md)
