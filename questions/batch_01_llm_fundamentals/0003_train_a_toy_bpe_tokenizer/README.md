# Q0003 · Train a toy BPE tokenizer

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Tokenization | Medium |

## Question

Implement BPE training: starting from characters, repeatedly merge the most frequent adjacent pair across a word-frequency corpus for `num_merges` steps. Return the ordered list of merges.

## Answer

Approach: represent each word as a tuple of symbols with its corpus count. At each step, count adjacent pairs weighted by word frequency, pick the most frequent (breaking ties deterministically), and rewrite every word by fusing that pair.

```python
from collections import Counter


def train_bpe(word_counts: dict[str, int], num_merges: int) -> list[tuple[str, str]]:
    vocab = {tuple(w): c for w, c in word_counts.items()}
    merges: list[tuple[str, str]] = []
    for _ in range(num_merges):
        pairs: Counter[tuple[str, str]] = Counter()
        for symbols, count in vocab.items():
            for a, b in zip(symbols, symbols[1:]):
                pairs[(a, b)] += count
        if not pairs:
            break
        best = max(pairs, key=lambda p: (pairs[p], p))
        merges.append(best)
        new_vocab: dict[tuple[str, ...], int] = {}
        for symbols, count in vocab.items():
            out, i = [], 0
            while i < len(symbols):
                if i + 1 < len(symbols) and (symbols[i], symbols[i + 1]) == best:
                    out.append(symbols[i] + symbols[i + 1])
                    i += 2
                else:
                    out.append(symbols[i])
                    i += 1
            new_vocab[tuple(out)] = new_vocab.get(tuple(out), 0) + count
        vocab = new_vocab
    return merges


corpus = {"low": 5, "lower": 2, "newest": 6, "widest": 3}
merges = train_bpe(corpus, 4)
assert merges[0] == ("s", "t")
assert merges[1] == ("e", "st")
assert len(merges) == 4
```

Complexity: O(merges × total symbols) for this naive version. Production trainers (Hugging Face `tokenizers`, `tiktoken`) use incremental pair counts and priority queues.

Real tokenizers also pre-tokenize (split on whitespace and punctuation with a regex) and run over bytes, not characters.

## Likely follow-ups

- Why do real BPE tokenizers work on bytes?
- How does Unigram (SentencePiece) differ from BPE?

---

[← Q0002](../../batch_01_llm_fundamentals/0002_why_subword_tokenization/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0004 →](../../batch_01_llm_fundamentals/0004_encode_text_with_learned_bpe_merges/README.md)
