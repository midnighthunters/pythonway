# Q0297 · End-to-end mini RAG pipeline

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | RAG implementation | Hard |

## Question

Implement a minimal but complete RAG pipeline in one function: entitlement filtering, BM25-style scoring, a relevance gate, numbered sources, generation with a (fake) LLM, and citation validation. Test the answer, abstention and entitlement cases.

## Answer

```python
import math
import re
from collections import Counter
from typing import Callable

tok = lambda s: re.findall(r"[a-z0-9]+", s.lower())


def rag_answer(question: str, chunks: list[dict], user_groups: set[str], llm: Callable[[str], str],
               k: int = 3, min_score: float = 0.5) -> dict:
    visible = [c for c in chunks if user_groups & set(c["acl"])]
    if not visible:
        return {"status": "not_found", "answer": "No accessible documents.", "sources": []}
    df = Counter(t for c in visible for t in set(tok(c["text"])))
    n = len(visible)
    idf = lambda t: math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
    scored = sorted(((sum(idf(t) for t in set(tok(question)) if t in set(tok(c["text"]))), c) for c in visible),
                    key=lambda x: -x[0])
    top = [c for s, c in scored[:k] if s >= min_score]
    if not top:
        return {"status": "not_found", "answer": "I couldn't find this in the documents you have access to.",
                "sources": []}
    sources = "\n".join(f"[{i}] {c['text']}" for i, c in enumerate(top, 1))
    answer = llm(f"Sources:\n{sources}\n\nQuestion: {question}\nCite as [n].")
    cited = {int(x) for x in re.findall(r"\[(\d+)\]", answer)}
    if not cited or not cited <= set(range(1, len(top) + 1)):
        return {"status": "rejected", "answer": "The answer failed citation checks.", "sources": []}
    return {"status": "answered", "answer": answer, "sources": [top[i - 1]["id"] for i in sorted(cited)]}


chunks = [{"id": "pol-7", "acl": ["all"], "text": "London hotels are capped at 180 GBP per night."},
          {"id": "hr-9", "acl": ["hr"], "text": "London salary bands for vice presidents."},
          {"id": "faq-2", "acl": ["all"], "text": "Expense claims are filed within 30 days."}]
fake_llm = lambda prompt: "The cap is 180 GBP per night [1]." if "180 GBP" in prompt else "Unknown."
ok = rag_answer("What is the London hotel cap?", chunks, {"all"}, fake_llm)
assert ok == {"status": "answered", "answer": "The cap is 180 GBP per night [1].", "sources": ["pol-7"]}
assert rag_answer("What is the parental leave policy?", chunks, {"all"}, fake_llm)["status"] == "not_found"
leak = rag_answer("London salary bands", chunks, {"all"}, lambda p: "hr-9 says... [1]" if "salary" in p else "no [1]")
assert "hr-9" not in leak["sources"] and "salary bands" not in str(leak)
```

Each stage here maps to a production component: the ACL filter to the search engine's security trimming, the IDF scoring to BM25 plus vectors plus a reranker, the gate to a calibrated threshold, and the citation check to output validation. Being able to write this skeleton in 20 minutes is a realistic Round 1 exercise for an AI engineer.

## Likely follow-ups

- Which stage would you replace first to improve quality, and how would you measure it?

---

[← Q0296](../../batch_03_rag_retrieval/0296_streaming_rag_answers_with_citations/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0298 →](../../batch_03_rag_retrieval/0298_rag_failure_mode_checklist/README.md)
