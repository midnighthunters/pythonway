# Q0023 · Beam search

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Decoding | Medium |

## Question

Implement beam search with beam width B over a function returning log-probabilities for the next token, with length normalisation. When would you use it for LLMs?

## Answer

```python
import math


def beam_search(next_logprobs, bos: int, eos: int, beam: int, max_len: int, alpha: float = 0.7):
    beams = [([bos], 0.0)]
    finished = []
    for _ in range(max_len):
        candidates = []
        for seq, score in beams:
            for tok, lp in next_logprobs(seq).items():
                candidates.append((seq + [tok], score + lp))
        candidates.sort(key=lambda c: c[1], reverse=True)
        beams = []
        for seq, score in candidates:
            (finished if seq[-1] == eos else beams).append((seq, score))
            if len(beams) == beam:
                break
        if not beams:
            break
    finished.extend(beams)
    return max(finished, key=lambda c: c[1] / (len(c[0]) - 1) ** alpha)


TABLE = {
    (0,): {1: math.log(0.6), 2: math.log(0.4)},
    (0, 1): {3: math.log(0.3), 9: math.log(0.7)},
    (0, 2): {3: math.log(0.9), 9: math.log(0.1)},
}


def model(seq):
    return TABLE.get(tuple(seq), {9: 0.0})


seq, score = beam_search(model, bos=0, eos=9, beam=2, max_len=3)
assert seq == [0, 2, 3, 9]
assert math.isclose(score, math.log(0.4 * 0.9))
```

Greedy picks token 1 first (0.6), but the best full sequence goes through token 2 (0.4 × 0.9 = 0.36 versus 0.6 × 0.3 = 0.18 for the three-token path). Beam search recovers it.

For chat LLMs, beam search is rarely used. It is expensive (B× compute), produces bland and repetitive text, and hosted APIs don't expose it. It remains useful for translation, ASR and constrained tasks.

## Likely follow-ups

- Why is length normalisation needed?

---

[← Q0022](../../batch_01_llm_fundamentals/0022_frequency_and_presence_penalties/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0024 →](../../batch_01_llm_fundamentals/0024_log_probabilities_as_confidence_signals/README.md)
