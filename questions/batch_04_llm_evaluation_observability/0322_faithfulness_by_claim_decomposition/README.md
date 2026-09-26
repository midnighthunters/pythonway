# Q0322 · Faithfulness by claim decomposition

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | RAG evaluation | Medium |

## Question

Implement a faithfulness metric: split the answer into atomic claims (with an LLM), check each claim against the retrieved context (with an entailment judge), and report the supported fraction and the unsupported claims.

## Answer

```python
import json
from typing import Callable


def faithfulness(answer: str, context: str, extract_claims: Callable[[str], str],
                 entails: Callable[[str, str], bool]) -> dict:
    claims = [c for c in json.loads(extract_claims(answer)) if isinstance(c, str) and c.strip()]
    if not claims:
        return {"score": 1.0, "unsupported": [], "n_claims": 0}
    unsupported = [c for c in claims if not entails(context, c)]
    return {"score": 1 - len(unsupported) / len(claims), "unsupported": unsupported, "n_claims": len(claims)}


context = "London hotels are capped at 180 GBP per night. Claims are filed within 30 days."
fake_claims = lambda a: json.dumps(["London hotels are capped at 180 GBP per night",
                                    "Claims are filed within 45 days", "Breakfast is included"])
fake_entails = lambda ctx, claim: claim.lower() in ctx.lower()
r = faithfulness("...", context, fake_claims, fake_entails)
assert abs(r["score"] - 1 / 3) < 1e-12
assert r["unsupported"] == ["Claims are filed within 45 days", "Breakfast is included"]
```

This is the approach behind RAGAS-style faithfulness. The per-claim list is more actionable than a single score, because it shows exactly what was hallucinated. The costs are two or more LLM calls per answer, so sample in production and run fully offline. Validate the claim extractor and entailment judge against human labels too.

## Likely follow-ups

- Why is "not supported by context" different from "false"?

---

[← Q0321](../../batch_04_llm_evaluation_observability/0321_calibrate_a_judge_against_human_labels/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0323 →](../../batch_04_llm_evaluation_observability/0323_answer_relevance_metric/README.md)
