# Q0325 · Citation accuracy metric

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | RAG evaluation | Medium |

## Question

Implement citation precision (the fraction of citations whose source supports the sentence) and citation recall (the fraction of claim sentences with at least one supporting citation).

## Answer

```python
import re
from typing import Callable


def citation_metrics(answer: str, sources: dict[int, str], supports: Callable[[str, str], bool]) -> dict:
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", answer.strip()) if s]
    total_cites = good_cites = supported_sentences = 0
    for s in sentences:
        cites = [int(n) for n in re.findall(r"\[(\d+)\]", s)]
        claim = re.sub(r"\s*\[\d+\]", "", s)
        ok = [n for n in cites if n in sources and supports(sources[n], claim)]
        total_cites += len(cites)
        good_cites += len(ok)
        supported_sentences += bool(ok)
    return {"precision": good_cites / total_cites if total_cites else 0.0,
            "recall": supported_sentences / len(sentences) if sentences else 0.0}


sources = {1: "London hotels are capped at 180 GBP.", 2: "Claims are filed within 30 days."}
supports = lambda src, claim: all(w in src.lower() for w in re.findall(r"[a-z0-9]+", claim.lower()) if len(w) > 3)
ans = "London hotels are capped at 180 GBP [1][2]. Claims are filed within 30 days [2]. Taxis are free."
m = citation_metrics(ans, sources, supports)
assert abs(m["precision"] - 2 / 3) < 1e-12 and abs(m["recall"] - 2 / 3) < 1e-12
```

Precision catches decorative or wrong citations. Recall catches uncited claims. Both matter for trust in a bank, because users are told to verify through the citations.

## Likely follow-ups

- Should a sentence such as "Here's what I found:" count as a claim?

---

[← Q0324](../../batch_04_llm_evaluation_observability/0324_context_precision_and_context_recall/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0326 →](../../batch_04_llm_evaluation_observability/0326_abstention_quality_metrics/README.md)
