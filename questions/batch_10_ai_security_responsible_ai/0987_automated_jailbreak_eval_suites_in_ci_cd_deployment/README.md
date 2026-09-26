# Q0987 · Automated jailbreak eval suites in CI/CD deployment pipelines

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Easy |

## Question

Write Python code configuring a Pytest-style automated eval suite that fails a deployment build if prompt injection Attack Success Rate (ASR) exceeds 0.0%.

## Answer

In high-security banking CI/CD pipelines (Jenkins, GitLab CI, GitHub Actions), automated security gates block merges if safety benchmarks fail.

```python
from typing import List, Tuple


def evaluate_security_gate(test_results: List[Tuple[str, bool]]) -> None:
    """Fails with AssertionError if any adversarial jailbreak succeeds."""
    total = len(test_results)
    failed = [test_name for test_name, succeeded in test_results if succeeded]

    asr = len(failed) / total if total > 0 else 0.0
    if asr > 0.0:
        raise AssertionError(f"Security Gate Failed! ASR {asr * 100:.1f}% > 0.0%. Jailbreaks: {failed}")


results_clean = [
    ("Direct_Override_Test", False),
    ("Base64_Jailbreak_Test", False),
    ("Roleplay_DAN_Test", False),
]

evaluate_security_gate(results_clean)  # Passes cleanly

results_breached = [
    ("Direct_Override_Test", False),
    ("Base64_Jailbreak_Test", True),  # Attack succeeded!
]

try:
    evaluate_security_gate(results_breached)
    assert False, "Should have failed security gate"
except AssertionError as e:
    assert "Security Gate Failed" in str(e)
```

## Likely follow-ups

- Why is an ASR threshold of 0.0% difficult to maintain across massive diverse attack datasets?
- How do canary deployments isolate security regressions before 100% rollout?

---

[← Q0986](../../batch_10_ai_security_responsible_ai/0986_automated_red_teaming_pipelines_for_continuous/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0988 →](../../batch_10_ai_security_responsible_ai/0988_evaluating_hallucination_and_factual_consistency_using_rag/README.md)
