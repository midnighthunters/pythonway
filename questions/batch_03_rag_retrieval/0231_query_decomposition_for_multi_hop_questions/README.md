# Q0231 · Query decomposition for multi-hop questions

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Query understanding | Medium |

## Question

"Which of our UK entities is subject to the policy that replaced POL-12?" needs two retrieval hops. Implement decomposition into ordered sub-questions, where later questions can use earlier answers.

## Answer

```python
import json
from typing import Callable


def decompose_and_answer(question: str, llm: Callable[[str], str], answer_with_rag: Callable[[str], str],
                         max_steps: int = 4) -> dict:
    steps = json.loads(llm(f"Split into ordered sub-questions (JSON list). Use {{prev}} for the prior answer: {question}"))
    if not isinstance(steps, list) or not steps or len(steps) > max_steps:
        raise ValueError("bad decomposition")
    trace, prev = [], ""
    for sub in steps:
        q = sub.replace("{prev}", prev)
        prev = answer_with_rag(q)
        trace.append((q, prev))
    return {"answer": prev, "trace": trace}


fake_llm = lambda p: json.dumps(["Which policy replaced POL-12?", "Which UK entities are subject to {prev}?"])
KB = {"Which policy replaced POL-12?": "POL-31",
      "Which UK entities are subject to POL-31?": "JPM Europe Ltd and JPM Securities plc"}
out = decompose_and_answer("...", fake_llm, lambda q: KB.get(q, "unknown"))
assert out["answer"] == "JPM Europe Ltd and JPM Securities plc"
assert out["trace"][1][0] == "Which UK entities are subject to POL-31?"
```

Agentic RAG generalises this: the model decides iteratively what to search for next. Cap the number of steps, stop when a hop returns "unknown", and show the trace for transparency.

## Likely follow-ups

- How do you stop an error in hop 1 from producing a confident wrong final answer?

---

[← Q0230](../../batch_03_rag_retrieval/0230_hypothetical_document_embeddings/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0232 →](../../batch_03_rag_retrieval/0232_extract_metadata_filters_from_queries/README.md)
