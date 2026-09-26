# Q0242 · Lexical groundedness check

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Grounding | Medium |

## Question

Implement a cheap groundedness check: for each answer sentence, measure how many of its content words appear in the sources it cites, and require that every number in the sentence appears in those sources. Flag weak sentences.

## Answer

```python
import re

STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "for", "on", "with", "be", "must", "per"}
CITE = re.compile(r"\[(\d+)\]")


def groundedness(answer: str, sources: dict[int, str], threshold: float = 0.6) -> list[dict]:
    report = []
    for sent in re.split(r"(?<=[.!?])\s+", answer.strip()):
        cited = [int(n) for n in CITE.findall(sent)]
        src = " ".join(sources.get(n, "") for n in cited).lower()
        text = CITE.sub("", sent).lower()
        words = [w for w in re.findall(r"[a-z]+", text) if w not in STOP and len(w) > 2]
        support = sum(w in src for w in words) / len(words) if words else 1.0
        numbers_ok = all(n in src for n in re.findall(r"\d+(?:\.\d+)?", text))
        report.append({"sentence": sent, "support": round(support, 2), "numbers_ok": numbers_ok,
                       "flag": not cited or support < threshold or not numbers_ok})
    return report


sources = {1: "Hotels in London are capped at 180 GBP per night.", 2: "Claims must be filed within 30 days."}
rep = groundedness("London hotels are capped at 180 GBP [1]. Claims must be filed within 45 days [2]. "
                   "Upgrades are always free.", sources)
assert [r["flag"] for r in rep] == [False, True, True]
assert rep[1]["numbers_ok"] is False
```

This catches wrong numbers and uncited claims cheaply, and it can run on every response. It misses paraphrased contradictions and negation errors. For those, sample responses for an NLI model or LLM-judge faithfulness check.

## Likely follow-ups

- Give an example sentence that passes this check but is still unfaithful.

---

[← Q0241](../../batch_03_rag_retrieval/0241_rag_answer_prompt_builder/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0243 →](../../batch_03_rag_retrieval/0243_hit_rate_and_mrr_for_a_retriever/README.md)
