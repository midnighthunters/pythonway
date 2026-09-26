# Q0990 · Toxicity, hate speech, and brand reputation filtering using guardrail models

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Easy |

## Question

Write Python code configuring Azure AI Content Safety / Llama Guard category severity thresholds to block hate speech, violence, and brand harm.

## Answer

Enterprise customer interactions must never output toxic language, defamatory statements, or offensive material. Content safety filters evaluate incoming and outgoing text across standardized severity categories (0 to 6), blocking any message exceeding corporate risk tolerances.

```python
from typing import Any, Dict


class ContentSafetyPolicyFilter:
    def __init__(self, max_allowed_severity: int = 2):
        self.max_severity = max_allowed_severity

    def evaluate_content_scores(self, category_scores: Dict[str, int]) -> Dict[str, Any]:
        """category_scores: dict mapping category name to severity (0: safe, 6: extreme)."""
        blocked_categories = []
        for cat, score in category_scores.items():
            if score > self.max_severity:
                blocked_categories.append((cat, score))

        is_safe = len(blocked_categories) == 0
        return {
            "is_safe": is_safe,
            "action": "ALLOW" if is_safe else "BLOCK",
            "violations": blocked_categories,
        }


policy = ContentSafetyPolicyFilter(max_allowed_severity=1)

# Safe interaction (severity 0)
scores_good = {"Hate": 0, "Violence": 0, "SelfHarm": 0, "Sexual": 0}
assert policy.evaluate_content_scores(scores_good)["action"] == "ALLOW"

# Harmful interaction (severity 4 Hate)
scores_bad = {"Hate": 4, "Violence": 0, "SelfHarm": 0, "Sexual": 0}
res_bad = policy.evaluate_content_scores(scores_bad)
assert res_bad["action"] == "BLOCK"
assert res_bad["violations"] == [("Hate", 4)]
```

## Likely follow-ups

- What are the differences between Azure AI Content Safety and open-weight Llama Guard 3?
- How do you tune thresholds to avoid false positives on legitimate financial discussions (e.g. "market execution", "bond slaughter")?

---

[← Q0989](../../batch_10_ai_security_responsible_ai/0989_bias_and_fairness_testing_in_credit_scoring_and_loan/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0991 →](../../batch_10_ai_security_responsible_ai/0991_nemo_guardrails_colang_programmable_dialog_rails/README.md)
