# Q0992 · LLM as a Judge: Designing reliable evaluation rubrics and inter-annotator agreement

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Hard |

## Question

Explain the LLM-as-a-Judge evaluation paradigm, and write Python code implementing an automated rubric-based grading evaluator with Cohen's Kappa inter-judge agreement.

## Answer

Using strong models (GPT-4o) to grade outputs of smaller or specialized models is standard practice in model evaluation. However, judges suffer from:
1. **Position Bias**: Favoring the first response presented.
2. **Verbosity Bias**: Favoring longer, wordier answers.
3. **Self-Enhancement Bias**: Favoring answers produced by models of the same family.

Rigorous evaluation requires standardized numerical rubrics (1 to 5) and measuring agreement across independent evaluations.

```python
def cohens_kappa(judge1_scores: list[int], judge2_scores: list[int]) -> float:
    """Calculates Cohen's Kappa inter-annotator agreement for 2 judges."""
    assert len(judge1_scores) == len(judge2_scores)
    n = len(judge1_scores)
    if n == 0:
        return 1.0

    # Observed agreement
    observed_agree = sum(1 for a, b in zip(judge1_scores, judge2_scores) if a == b) / n

    # Chance agreement
    categories = set(judge1_scores + judge2_scores)
    expected_agree = 0.0
    for c in categories:
        p1 = judge1_scores.count(c) / n
        p2 = judge2_scores.count(c) / n
        expected_agree += p1 * p2

    if expected_agree == 1.0:
        return 1.0
    kappa = (observed_agree - expected_agree) / (1.0 - expected_agree)
    return round(kappa, 4)


# Both judges agree on most evaluations
j1 = [1, 2, 1, 2, 1, 1, 2]
j2 = [1, 2, 1, 2, 1, 2, 2]  # Disagrees on 1 case

k = cohens_kappa(j1, j2)
assert k > 0.60  # Substantial agreement
```

## Likely follow-ups

- How does pairwise comparison with position swapping eliminate position bias in LLM judges?
- How do human-in-the-loop spot-checks calibrate LLM judge accuracy?

---

[← Q0991](../../batch_10_ai_security_responsible_ai/0991_nemo_guardrails_colang_programmable_dialog_rails/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0993 →](../../batch_10_ai_security_responsible_ai/0993_semantic_drift_detection_and_output_distribution_shifts_in/README.md)
