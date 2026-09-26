# Q0054 · Truncate text to a token budget

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Context management | Medium |

## Question

Given a tokenizer interface with `encode` and `decode`, truncate a document to a token budget using a head, tail or middle strategy (keep the start and end, drop the middle with a marker).

## Answer

Why it matters here: when a document or tool output is too long for the context, which part you keep matters. Logs often need the tail, contracts the head, and transcripts both ends.

```python
from typing import Protocol


class Tokenizer(Protocol):
    def encode(self, text: str) -> list[int]: ...
    def decode(self, ids: list[int]) -> str: ...


class WhitespaceTokenizer:
    def __init__(self) -> None:
        self.vocab: dict[str, int] = {}
        self.inv: dict[int, str] = {}

    def encode(self, text: str) -> list[int]:
        ids = []
        for w in text.split():
            if w not in self.vocab:
                self.vocab[w] = len(self.vocab)
                self.inv[self.vocab[w]] = w
            ids.append(self.vocab[w])
        return ids

    def decode(self, ids: list[int]) -> str:
        return " ".join(self.inv[i] for i in ids)


def truncate_tokens(text: str, tok: Tokenizer, budget: int, strategy: str = "middle",
                    marker: str = "[...truncated...]") -> str:
    ids = tok.encode(text)
    if len(ids) <= budget:
        return text
    marker_len = len(tok.encode(marker))
    if strategy == "head":
        return tok.decode(ids[:budget])
    if strategy == "tail":
        return tok.decode(ids[-budget:])
    keep = budget - marker_len
    if keep <= 0:
        raise ValueError("budget too small for marker")
    head = keep // 2 + keep % 2
    return f"{tok.decode(ids[:head])} {marker} {tok.decode(ids[-(keep - head):])}"


tok = WhitespaceTokenizer()
doc = " ".join(f"w{i}" for i in range(20))
assert truncate_tokens(doc, tok, 5, "head") == "w0 w1 w2 w3 w4"
assert truncate_tokens(doc, tok, 3, "tail") == "w17 w18 w19"
mid = truncate_tokens(doc, tok, 6, "middle")
assert mid == "w0 w1 w2 [...truncated...] w18 w19"
assert len(tok.encode(mid)) == 6
assert truncate_tokens("short text", tok, 10) == "short text"
```

With a real BPE tokenizer, decoding a slice can split a multi-byte character or a word. Decode with error handling, or cut on token boundaries that align with whitespace.

## Likely follow-ups

- When is summarisation better than truncation, and what does it cost?

---

[← Q0053](../../batch_01_llm_fundamentals/0053_tokenization_cost_surprises/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0055 →](../../batch_01_llm_fundamentals/0055_padding_side_for_batched_generation/README.md)
