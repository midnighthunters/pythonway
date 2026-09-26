# Q0326 · Abstention quality metrics

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Reliability evaluation | Medium |

## Question

Implement metrics for abstention: abstention precision and recall (on cases that should abstain), and the false-abstention rate on answerable cases.

## Answer

```python
def abstention_metrics(cases: list[dict]) -> dict:
    """cases: {'should_abstain': bool, 'abstained': bool}"""
    tp = sum(c["should_abstain"] and c["abstained"] for c in cases)
    fp = sum(not c["should_abstain"] and c["abstained"] for c in cases)
    fn = sum(c["should_abstain"] and not c["abstained"] for c in cases)
    answerable = sum(not c["should_abstain"] for c in cases)
    return {"abstain_precision": tp / (tp + fp) if tp + fp else 0.0,
            "abstain_recall": tp / (tp + fn) if tp + fn else 0.0,
            "false_abstention_rate": fp / answerable if answerable else 0.0}


cases = ([{"should_abstain": True, "abstained": True}] * 8 + [{"should_abstain": True, "abstained": False}] * 2
         + [{"should_abstain": False, "abstained": True}] * 5 + [{"should_abstain": False, "abstained": False}] * 85)
m = abstention_metrics(cases)
assert m["abstain_recall"] == 0.8 and abs(m["abstain_precision"] - 8 / 13) < 1e-12
assert abs(m["false_abstention_rate"] - 5 / 90) < 1e-12
```

Abstain recall measures safety (does it avoid hallucinating when it can't know?), and the false-abstention rate measures usefulness. Tune prompts and retrieval thresholds against both, and set targets per use case. A compliance assistant tolerates more false abstentions than a general helpdesk bot.

## Likely follow-ups

- Which failure is worse for a policy assistant, and why?

---

[← Q0325](../../batch_04_llm_evaluation_observability/0325_citation_accuracy_metric/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0327 →](../../batch_04_llm_evaluation_observability/0327_build_a_safety_evaluation_set/README.md)
