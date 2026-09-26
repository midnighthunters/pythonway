# Q0004 · Encode text with learned BPE merges

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Tokenization | Medium |

## Question

Given an ordered merge list (earlier merges have higher priority), encode a word by repeatedly applying the highest-priority merge present, until none apply.

## Answer

Approach: rank each merge by its index. At each step, find the adjacent pair with the lowest rank and merge every occurrence of it. This is how GPT-2-style BPE encoding works.

```python
def bpe_encode(word: str, merges: list[tuple[str, str]]) -> list[str]:
    rank = {pair: i for i, pair in enumerate(merges)}
    symbols = list(word)
    while len(symbols) > 1:
        candidates = [(rank[p], i) for i, p in enumerate(zip(symbols, symbols[1:])) if p in rank]
        if not candidates:
            break
        best_rank, _ = min(candidates)
        best = merges[best_rank]
        out, i = [], 0
        while i < len(symbols):
            if i + 1 < len(symbols) and (symbols[i], symbols[i + 1]) == best:
                out.append(symbols[i] + symbols[i + 1])
                i += 2
            else:
                out.append(symbols[i])
                i += 1
        symbols = out
    return symbols


merges = [("s", "t"), ("e", "st"), ("l", "o"), ("lo", "w"), ("n", "e"), ("ne", "w")]
assert bpe_encode("lowest", merges) == ["low", "est"]
assert bpe_encode("newest", merges) == ["new", "est"]
assert bpe_encode("xyz", merges) == ["x", "y", "z"]
assert "".join(bpe_encode("slowest", merges)) == "slowest"
```

Complexity: O(n²) per word in this simple version. Real encoders cache results per pre-token.

Invariant worth testing: joining the tokens always reproduces the input (lossless).

## Likely follow-ups

- Why must merges be applied in training order rather than greedily by length?
- How would you make this fast for millions of requests (caching, a Rust tokenizer)?

---

[← Q0003](../../batch_01_llm_fundamentals/0003_train_a_toy_bpe_tokenizer/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0005 →](../../batch_01_llm_fundamentals/0005_estimate_request_cost_from_token_usage/README.md)
