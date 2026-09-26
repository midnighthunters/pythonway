# Q0079 · Bigram language model with smoothing

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Language modelling | Medium |

## Question

Implement a bigram language model with add-k smoothing: training, next-word probability, perplexity and greedy generation. What does it teach about modern LLMs?

## Answer

```python
import math
from collections import Counter, defaultdict


class BigramLM:
    def __init__(self, corpus: list[list[str]], k: float = 1.0) -> None:
        self.k = k
        self.vocab = {"</s>"} | {w for s in corpus for w in s}
        self.counts: dict[str, Counter] = defaultdict(Counter)
        for s in corpus:
            toks = ["<s>", *s, "</s>"]
            for a, b in zip(toks, toks[1:]):
                self.counts[a][b] += 1

    def prob(self, prev: str, word: str) -> float:
        c = self.counts[prev]
        return (c[word] + self.k) / (sum(c.values()) + self.k * len(self.vocab))

    def perplexity(self, sentence: list[str]) -> float:
        toks = ["<s>", *sentence, "</s>"]
        lp = sum(math.log(self.prob(a, b)) for a, b in zip(toks, toks[1:]))
        return math.exp(-lp / (len(toks) - 1))

    def greedy(self, max_len: int = 10) -> list[str]:
        out, prev = [], "<s>"
        for _ in range(max_len):
            nxt = max(sorted(self.vocab), key=lambda w: self.prob(prev, w))
            if nxt == "</s>":
                break
            out.append(nxt)
            prev = nxt
        return out


lm = BigramLM([["the", "cat", "sat"], ["the", "dog", "sat"], ["the", "cat", "ran"]])
assert math.isclose(sum(lm.prob("<s>", w) for w in lm.vocab), 1.0)
assert lm.greedy() == ["the", "cat", "ran"]
assert lm.perplexity(["the", "cat", "sat"]) < lm.perplexity(["dog", "the", "ran"])
assert lm.prob("cat", "flew") > 0
```

Lessons: an LLM is the same "predict the next token" idea with a vastly better model of context. Smoothing is why unseen continuations still get non-zero probability. Perplexity measures fit. Greedy decoding picks deterministic but not always sensible continuations.

## Likely follow-ups

- Why does an n-gram model fail as n grows (sparsity), and how do neural models avoid that?

---

[← Q0078](../../batch_01_llm_fundamentals/0078_alternatives_to_quadratic_attention/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0080 →](../../batch_01_llm_fundamentals/0080_utf_8_bytes_and_safe_truncation/README.md)
