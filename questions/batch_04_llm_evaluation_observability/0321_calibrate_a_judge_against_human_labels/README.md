# Q0321 · Calibrate a judge against human labels

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Model-graded evaluation | Medium |

## Question

Compare an LLM judge's pass/fail verdicts with SME labels: compute agreement, Cohen's kappa, and the judge's false-pass and false-fail rates, and decide whether the judge can gate releases.

## Answer

```python
from collections import Counter


def judge_calibration(human: list[str], judge: list[str], min_kappa: float = 0.6, max_false_pass: float = 0.1) -> dict:
    n = len(human)
    po = sum(h == j for h, j in zip(human, judge)) / n
    ch, cj = Counter(human), Counter(judge)
    pe = sum(ch[k] * cj[k] for k in ch.keys() | cj.keys()) / n ** 2
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    human_fail = [j for h, j in zip(human, judge) if h == "fail"]
    human_pass = [j for h, j in zip(human, judge) if h == "pass"]
    false_pass = human_fail.count("pass") / len(human_fail) if human_fail else 0.0
    false_fail = human_pass.count("fail") / len(human_pass) if human_pass else 0.0
    usable = kappa >= min_kappa and false_pass <= max_false_pass
    return {"agreement": po, "kappa": round(kappa, 3), "false_pass": false_pass, "false_fail": false_fail,
            "usable_for_gating": usable}


human = ["pass"] * 14 + ["fail"] * 6
judge = ["pass"] * 13 + ["fail"] + ["fail"] * 5 + ["pass"]
r = judge_calibration(human, judge)
assert r["agreement"] == 0.9 and r["false_pass"] == 1 / 6 and not r["usable_for_gating"]
```

90% agreement looks good, but the judge passes one in six answers the SMEs failed, which is too lenient to gate a release. Improve the rubric, add examples of failing answers, or use a stronger judge, then re-measure on a fresh sample. For gating, false passes usually matter more than false fails.

## Likely follow-ups

- How many human-labelled examples do you need for this calibration to be trustworthy?

---

[← Q0320](../../batch_04_llm_evaluation_observability/0320_known_biases_of_llm_judges/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0322 →](../../batch_04_llm_evaluation_observability/0322_faithfulness_by_claim_decomposition/README.md)
