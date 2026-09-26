# Q0147 · Automatic prompt optimisation with an eval loop

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt optimisation | Medium |

## Question

Implement a simple prompt optimiser: score candidate prompts on a dev split, choose the best (ties go to the shorter prompt), and report its score on a held-out test split to avoid over-fitting.

## Answer

```python
from typing import Callable


def accuracy(prompt: str, cases: list[tuple[str, str]], llm: Callable[[str, str], str]) -> float:
    return sum(llm(prompt, x).strip() == y for x, y in cases) / len(cases)


def select_prompt(candidates: list[str], dev: list[tuple[str, str]], test: list[tuple[str, str]],
                  llm: Callable[[str, str], str]) -> dict:
    scored = [(accuracy(p, dev, llm), -len(p), p) for p in candidates]
    dev_score, _, best = max(scored)
    return {"prompt": best, "dev": dev_score, "test": accuracy(best, test, llm),
            "all_dev": {p: s for s, _, p in scored}}


def fake_llm(prompt: str, x: str) -> str:
    if "label definitions" in prompt:
        return "refund" if "money back" in x or "refund" in x else "other"
    return "refund" if "refund" in x else "other"


dev = [("I want a refund", "refund"), ("money back please", "refund"), ("hello", "other")]
test = [("refund my fee", "refund"), ("give me my money back", "refund"), ("thanks", "other")]
res = select_prompt(["Classify.", "Classify using the label definitions below.",
                     "Classify carefully using the label definitions below."], dev, test, fake_llm)
assert res["prompt"] == "Classify using the label definitions below."
assert res["dev"] == 1.0 and res["test"] == 1.0
```

The two best prompts tie on dev, so the shorter one wins. Frameworks such as DSPy automate this search (instruction and example proposals, bootstrapped demonstrations). With small dev sets, differences of a few points are noise, so use enough cases and repeated runs.

## Likely follow-ups

- Why can "optimising" a prompt on 30 examples make production worse?

---

[← Q0146](../../batch_02_prompting_context_structured_output/0146_the_sandwich_defence_and_its_limits/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0148 →](../../batch_02_prompting_context_structured_output/0148_unit_tests_for_prompts/README.md)
