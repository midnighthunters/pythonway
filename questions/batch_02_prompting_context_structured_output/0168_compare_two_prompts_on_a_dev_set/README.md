# Q0168 · Compare two prompts on a dev set

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt evaluation | Medium |

## Question

Prompt B beats prompt A on 9 cases and loses on 1 (with 40 ties). Write a paired comparison with an exact two-sided sign test to judge whether the difference is likely real.

## Answer

Paired comparison on the same cases removes case difficulty from the picture. Only discordant cases (one prompt right, the other wrong) carry information.

```python
from math import comb


def sign_test_p(wins: int, losses: int) -> float:
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def compare_prompts(a_correct: list[bool], b_correct: list[bool]) -> dict:
    if len(a_correct) != len(b_correct):
        raise ValueError("results must be paired case-by-case")
    b_wins = sum(b and not a for a, b in zip(a_correct, b_correct))
    a_wins = sum(a and not b for a, b in zip(a_correct, b_correct))
    return {"b_wins": b_wins, "a_wins": a_wins, "ties": len(a_correct) - b_wins - a_wins,
            "p_value": sign_test_p(b_wins, a_wins)}


a = [False] * 9 + [True] + [True] * 20 + [False] * 20
b = [True] * 9 + [False] + [True] * 20 + [False] * 20
res = compare_prompts(a, b)
assert (res["b_wins"], res["a_wins"], res["ties"]) == (9, 1, 40)
assert abs(res["p_value"] - 22 / 1024) < 1e-12
assert sign_test_p(3, 2) > 0.5
```

p ≈ 0.02, so B's advantage is unlikely to be chance on this set. Still check that the cases are representative, repeat runs to account for non-determinism, and confirm on held-out data. For LLM-judge scores rather than pass/fail, use paired bootstrap confidence intervals.

## Likely follow-ups

- Why is an unpaired comparison of two accuracy numbers weaker here?

---

[← Q0167](../../batch_02_prompting_context_structured_output/0167_log_prompt_metadata_for_traceability/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0169 →](../../batch_02_prompting_context_structured_output/0169_combined_citation_and_abstention_template/README.md)
