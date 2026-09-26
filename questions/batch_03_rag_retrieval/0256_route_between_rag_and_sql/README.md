# Q0256 · Route between RAG and SQL

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Routing | Medium |

## Question

Implement a first-pass router that sends aggregation or metric questions to text-to-SQL, document questions to RAG, and mixed questions to both, and explain how you'd replace it with a learned router.

## Answer

```python
import re

AGG = re.compile(r"\b(total|sum|average|avg|how many|count|trend|by month|by quarter|top \d+|highest|lowest)\b", re.I)
METRICS = {"spend", "revenue", "headcount", "balance", "volume", "trades"}
DOC = re.compile(r"\b(policy|procedure|allowed|rule|guideline|how do i|what is the process)\b", re.I)


def route(question: str) -> set[str]:
    words = set(re.findall(r"[a-z]+", question.lower()))
    wants_sql = bool(AGG.search(question)) and bool(words & METRICS)
    wants_rag = bool(DOC.search(question))
    if wants_sql and wants_rag:
        return {"sql", "rag"}
    if wants_sql:
        return {"sql"}
    return {"rag"}


assert route("What was total travel spend by quarter in 2026?") == {"sql"}
assert route("Is business class allowed for a 7 hour flight?") == {"rag"}
assert route("How many trades breached the limit, and what does the policy say about breaches?") == {"sql", "rag"}
assert route("hello") == {"rag"}
```

Replace it with an LLM classifier (a structured output with enum routes) or a small trained classifier on labelled routing data, and keep the rules as a fallback. Log route decisions and outcomes, and evaluate routing accuracy separately from answer quality.

## Likely follow-ups

- What's the cost of a wrong route in each direction?

---

[← Q0255](../../batch_03_rag_retrieval/0255_entity_co_occurrence_graph_expansion/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0257 →](../../batch_03_rag_retrieval/0257_choose_long_context_or_retrieval_per_request/README.md)
