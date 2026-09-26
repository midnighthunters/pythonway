# Q0988 · Evaluating hallucination and factual consistency using RAG Triad

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Hard |

## Question

Explain the RAG Triad framework (Context Relevance, Groundedness/Faithfulness, and Answer Relevance), and write Python code calculating Faithfulness score via claim verification.

## Answer

The **RAG Triad** (popularized by TruLens) evaluates RAG pipelines across three independent axes:
1. **Context Relevance**: Did the vector retriever fetch documents truly relevant to the user query?
2. **Groundedness / Faithfulness**: Is every factual claim in the generated answer supported by the retrieved context?
3. **Answer Relevance**: Did the generated answer actually address the user's specific prompt?

```python
from typing import List


class FaithfulnessEvaluator:
    @staticmethod
    def calculate_faithfulness(claims: List[str], retrieved_context: str) -> float:
        if not claims:
            return 1.0
        supported = 0
        for claim in claims:
            # Check if claim keywords exist in source context
            words = [w.lower() for w in claim.split() if len(w) > 3]
            match_count = sum(1 for w in words if w in retrieved_context.lower())
            if match_count / len(words) >= 0.7:  # 70% keyword grounding threshold
                supported += 1

        return round(supported / len(claims), 4)


context = "JPMorgan Chase reported net revenue of $43.3 billion for the second quarter of 2024."
claims_valid = ["Net revenue was $43.3 billion", "Reported for the second quarter of 2024"]
score_valid = FaithfulnessEvaluator.calculate_faithfulness(claims_valid, context)
assert score_valid == 1.0

claims_hallucinated = ["Reported for the second quarter of 2024", "Net revenue declined by 15%"]
score_hallucinated = FaithfulnessEvaluator.calculate_faithfulness(claims_hallucinated, context)
assert score_hallucinated == 0.5
```

## Likely follow-ups

- How does using an LLM-as-a-judge improve claim verification over simple lexical keyword overlap?
- What are the trade-offs between RAGAS and TruLens evaluation frameworks?

---

[← Q0987](../../batch_10_ai_security_responsible_ai/0987_automated_jailbreak_eval_suites_in_ci_cd_deployment/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0989 →](../../batch_10_ai_security_responsible_ai/0989_bias_and_fairness_testing_in_credit_scoring_and_loan/README.md)
