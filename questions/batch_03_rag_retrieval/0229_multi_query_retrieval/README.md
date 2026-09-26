# Q0229 · Multi-query retrieval

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Query understanding | Medium |

## Question

Implement multi-query retrieval: generate several paraphrases of the question with an LLM, retrieve for each, and fuse the lists with RRF.

## Answer

```python
import json
from collections import defaultdict
from typing import Callable


def rrf(lists: list[list[str]], k: int = 60) -> list[str]:
    s: dict[str, float] = defaultdict(float)
    for lst in lists:
        for r, d in enumerate(lst, 1):
            s[d] += 1 / (k + r)
    return sorted(s, key=lambda d: (-s[d], d))


def multi_query(question: str, llm: Callable[[str], str], retrieve: Callable[[str], list[str]],
                n: int = 3, top_k: int = 5) -> list[str]:
    try:
        variants = [v for v in json.loads(llm(f"Give {n} alternative search queries as a JSON list: {question}"))
                    if isinstance(v, str) and v.strip()][:n]
    except (json.JSONDecodeError, TypeError):
        variants = []
    queries = [question, *variants]
    return rrf([retrieve(q) for q in queries])[:top_k]


INDEX = {"expense deadline": ["pol-exp"], "claim reimbursement time limit": ["pol-exp", "faq-9"],
         "how long to submit receipts": ["faq-9"]}
fake_llm = lambda p: json.dumps(["claim reimbursement time limit", "how long to submit receipts"])
out = multi_query("expense deadline", fake_llm, lambda q: INDEX.get(q, []))
assert out == ["pol-exp", "faq-9"]
assert multi_query("expense deadline", lambda p: "not json", lambda q: INDEX.get(q, [])) == ["pol-exp"]
```

It improves recall for vague or jargon-mismatched questions, at the cost of one LLM call plus several retrievals. Run the retrievals in parallel.

## Likely follow-ups

- When does multi-query hurt precision?

---

[← Q0228](../../batch_03_rag_retrieval/0228_condense_follow_up_questions/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0230 →](../../batch_03_rag_retrieval/0230_hypothetical_document_embeddings/README.md)
