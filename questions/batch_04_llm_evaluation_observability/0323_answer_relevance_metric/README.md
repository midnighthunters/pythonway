# Q0323 · Answer relevance metric

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | RAG evaluation | Medium |

## Question

How do you measure whether an answer actually addresses the question (as opposed to being faithful but off-topic)? Implement a simple version.

## Answer

One approach: generate the questions that the answer would be a good answer to, and measure their similarity to the original question. A judge asking "does this answer the question?" is the other common approach.

```python
import math
import re
from collections import Counter
from typing import Callable

STOP = {"the", "a", "is", "what", "for", "of", "in", "are", "how", "do", "i", "to"}


def vec(t: str) -> Counter:
    return Counter(w for w in re.findall(r"[a-z]+", t.lower()) if w not in STOP)


def cos(a: Counter, b: Counter) -> float:
    d = sum(a[k] * b[k] for k in a)
    na, nb = math.sqrt(sum(v * v for v in a.values())), math.sqrt(sum(v * v for v in b.values()))
    return d / (na * nb) if na and nb else 0.0


def answer_relevance(question: str, answer: str, gen_questions: Callable[[str], list[str]]) -> float:
    qs = gen_questions(answer)
    return sum(cos(vec(question), vec(q)) for q in qs) / len(qs) if qs else 0.0


GEN = {"The London hotel cap is 180 GBP per night.": ["What is the London hotel cap?", "Hotel cap London?"],
       "Our cafeteria opens at 8am.": ["When does the cafeteria open?"]}
q = "What is the hotel cap in London?"
on = answer_relevance(q, "The London hotel cap is 180 GBP per night.", GEN.get)
off = answer_relevance(q, "Our cafeteria opens at 8am.", GEN.get)
assert on > 0.8 and off == 0.0
```

Relevance and faithfulness are separate axes: a faithful answer can dodge the question, and a relevant answer can be hallucinated. Track both.

## Likely follow-ups

- How would you penalise answers that are relevant but incomplete?

---

[← Q0322](../../batch_04_llm_evaluation_observability/0322_faithfulness_by_claim_decomposition/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0324 →](../../batch_04_llm_evaluation_observability/0324_context_precision_and_context_recall/README.md)
