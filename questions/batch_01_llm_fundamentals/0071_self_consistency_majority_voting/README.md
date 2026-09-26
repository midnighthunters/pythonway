# Q0071 · Self-consistency majority voting

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Reasoning techniques | Medium |

## Question

Implement self-consistency: sample several answers, normalise them, return the majority answer and the agreement ratio (usable as a confidence score). Ties go to the answer seen first.

## Answer

```python
from collections import Counter


def normalize(answer: str) -> str:
    return " ".join(answer.strip().lower().rstrip(".").split())


def majority_vote(answers: list[str]) -> tuple[str, float]:
    if not answers:
        raise ValueError("no answers")
    norm = [normalize(a) for a in answers]
    counts = Counter(norm)
    best = max(counts.values())
    winner = next(a for a in norm if counts[a] == best)
    return winner, best / len(norm)


assert majority_vote(["42", "42.", " 41", "42"]) == ("42", 0.75)
assert majority_vote(["Paris", "London"]) == ("paris", 0.5)
```

Self-consistency improves accuracy on reasoning tasks with a single checkable answer (maths, classification, extraction), and the agreement ratio is a useful uncertainty signal for routing to human review. It costs N times the tokens. For free-form text, use a judge or an embedding-based cluster vote instead of exact match.

## Likely follow-ups

- How many samples are worth it, and how would you find out?

---

[← Q0070](../../batch_01_llm_fundamentals/0070_data_tensor_and_pipeline_parallelism/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0072 →](../../batch_01_llm_fundamentals/0072_why_chain_of_thought_helps/README.md)
