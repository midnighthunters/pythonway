# Q0770 · Evaluating hallucination scores against ground-truth context in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Write Python code that evaluates whether key entities in a generated answer exist in the provided RAG source context, flagging potential hallucinations.

## Answer

```python
import re
from typing import Any, Dict, List, Set


class GroundingFactChecker:
    @staticmethod
    def extract_entities(text: str) -> Set[str]:
        # Extract capitalized words and monetary/numerical terms
        tokens = re.findall(r"\b[A-Z][a-z0-9]+\b|\$\d+(?:,\d+)*(?:\.\d+)?|\b\d+%\b", text)
        return set(tokens)

    @classmethod
    def evaluate_grounding(cls, context: str, answer: str) -> Dict[str, Any]:
        context_lower = context.lower()
        answer_entities = cls.extract_entities(answer)

        unsupported = []
        for ent in answer_entities:
            if ent.lower() not in context_lower:
                unsupported.append(ent)

        total = len(answer_entities)
        score = (total - len(unsupported)) / total if total > 0 else 1.0

        return {
            "grounding_score": round(score, 2),
            "is_grounded": len(unsupported) == 0,
            "unsupported_entities": unsupported,
        }


ctx = "The bank JPMorgan reported Q3 net income of $13.2 billion and return on equity of 18%."
grounded_ans = "The bank achieved net income of $13.2 billion with 18% return."
hallucinated_ans = "The bank achieved net income of $15.5 billion with 22% return in London."

res_ok = GroundingFactChecker.evaluate_grounding(ctx, grounded_ans)
assert res_ok["is_grounded"] is True
assert res_ok["grounding_score"] == 1.0

res_bad = GroundingFactChecker.evaluate_grounding(ctx, hallucinated_ans)
assert res_bad["is_grounded"] is False
assert "$15.5" in res_bad["unsupported_entities"]
```

## Likely follow-ups

- What are the limitations of simple entity-matching compared to NLI (Natural Language Inference) models?
- How does RAG triad evaluation (faithfulness, answer relevance, context precision) relate to this check?

---

[← Q0769](../../batch_08_azure_openai_bedrock_cloud_ai/0769_bedrock_guardrails_contextual_grounding_evaluation/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0771 →](../../batch_08_azure_openai_bedrock_cloud_ai/0771_knowledge_bases_hybrid_search_bm25_plus_opensearch_vector/README.md)
