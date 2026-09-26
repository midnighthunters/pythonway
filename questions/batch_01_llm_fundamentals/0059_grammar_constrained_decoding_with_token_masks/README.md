# Q0059 · Grammar-constrained decoding with token masks

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Structured decoding | Hard |

## Question

Implement constrained greedy decoding that forces the output to match `^\d{1,3}$` by masking disallowed tokens at every step. Explain how structured-output features build on the same idea.

## Answer

At each step, compute the set of tokens that keep the output a valid prefix of the grammar, set every other logit to -inf, then pick or sample as usual. Servers and libraries (Outlines, XGrammar, llama.cpp grammars, provider "structured outputs" modes) compile a JSON Schema or regex into an automaton over the tokenizer's vocabulary to do this efficiently.

```python
import numpy as np

VOCAB = ["<eos>"] + [str(d) for d in range(10)] + ["a", " "]
EOS, DIGITS = 0, set(range(1, 11))


def allowed(prefix: str) -> set[int]:
    ids = set()
    if len(prefix) < 3:
        ids |= DIGITS
    if len(prefix) >= 1:
        ids.add(EOS)
    return ids


def constrained_greedy(logits_fn, max_steps: int = 10) -> str:
    out = ""
    for _ in range(max_steps):
        mask = np.full(len(VOCAB), -np.inf)
        mask[list(allowed(out))] = 0.0
        tok = int(np.argmax(logits_fn(out) + mask))
        if tok == EOS:
            break
        out += VOCAB[tok]
    return out


def prefers_letter(prefix: str) -> np.ndarray:
    logits = np.zeros(len(VOCAB))
    logits[11], logits[8], logits[EOS] = 5.0, 3.0, 1.0
    return logits


def prefers_stop(prefix: str) -> np.ndarray:
    logits = np.zeros(len(VOCAB))
    logits[EOS], logits[4] = 9.0, 2.0
    return logits


assert constrained_greedy(prefers_letter) == "777"
assert constrained_greedy(prefers_stop) == "3"
```

The model wanted "a", but the mask forced digits. After three digits, only EOS was legal.

Caveat: constraints guarantee syntax, not correctness. Forcing a schema the model is unsure about can yield confidently wrong values, so still validate semantics.

## Likely follow-ups

- Why is mapping a grammar onto BPE tokens (not characters) the hard part?

---

[← Q0058](../../batch_01_llm_fundamentals/0058_sources_of_non_determinism_in_llm_apis/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0060 →](../../batch_01_llm_fundamentals/0060_budget_max_tokens_against_the_context_window/README.md)
