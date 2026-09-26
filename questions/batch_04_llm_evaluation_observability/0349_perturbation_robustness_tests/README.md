# Q0349 · Perturbation robustness tests

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Testing | Medium |

## Question

Users make typos. Implement a seeded typo injector (swap, drop or duplicate characters) and measure the accuracy drop of a classifier on perturbed inputs.

## Answer

```python
import random
from typing import Callable


def add_typos(text: str, rate: float, rng: random.Random) -> str:
    chars = list(text)
    i = 0
    while i < len(chars):
        if chars[i].isalpha() and rng.random() < rate:
            op = rng.choice(["swap", "drop", "dup"])
            if op == "swap" and i + 1 < len(chars):
                chars[i], chars[i + 1] = chars[i + 1], chars[i]
                i += 1
            elif op == "drop":
                del chars[i]
                continue
            else:
                chars.insert(i, chars[i])
                i += 1
        i += 1
    return "".join(chars)


def robustness(classify: Callable[[str], str], cases: list[tuple[str, str]], rate: float, seed: int = 0) -> dict:
    rng = random.Random(seed)
    clean = sum(classify(x) == y for x, y in cases) / len(cases)
    noisy = sum(classify(add_typos(x, rate, rng)) == y for x, y in cases) / len(cases)
    return {"clean": clean, "noisy": noisy, "drop": clean - noisy}


keyword_clf = lambda t: "access" if "password" in t.lower() else "billing" if "invoice" in t.lower() else "other"
cases = [("I forgot my password", "access"), ("Where is my invoice", "billing"),
         ("Password expired again", "access"), ("Invoice total is wrong", "billing")] * 5
r = robustness(keyword_clf, cases, rate=0.15)
assert r["clean"] == 1.0 and r["drop"] > 0
assert add_typos("abc", 0.0, random.Random(1)) == "abc"
```

Keyword systems collapse under typos. LLMs are far more robust, but not perfectly so, especially for identifiers and numbers. Report robustness per perturbation type, and include realistic noise (mobile typos, mixed languages) in evaluation sets.

## Likely follow-ups

- Which perturbations should never change the answer, and which legitimately should?

---

[← Q0348](../../batch_04_llm_evaluation_observability/0348_metamorphic_testing_for_llm_systems/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0350 →](../../batch_04_llm_evaluation_observability/0350_slice_evaluation_results_by_segment/README.md)
