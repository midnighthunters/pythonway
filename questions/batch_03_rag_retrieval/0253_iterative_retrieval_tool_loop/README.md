# Q0253 · Iterative retrieval tool loop

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Agentic retrieval | Medium |

## Question

Implement a bounded agentic retrieval loop: at each step the model either issues `SEARCH: <query>` or `ANSWER: <text>`. Accumulate evidence, reject repeated queries, and stop at a step limit with a safe fallback.

## Answer

```python
from typing import Callable


def agentic_rag(question: str, llm: Callable[[str], str], search: Callable[[str], list[str]],
                max_steps: int = 4) -> dict:
    evidence: list[str] = []
    queries: list[str] = []
    for step in range(max_steps):
        prompt = f"Question: {question}\nEvidence:\n" + "\n".join(evidence) + "\nReply SEARCH: <q> or ANSWER: <a>"
        action = llm(prompt).strip()
        if action.startswith("ANSWER:"):
            return {"answer": action[7:].strip(), "queries": queries, "steps": step + 1}
        if action.startswith("SEARCH:"):
            q = action[7:].strip()
            if q.lower() in (x.lower() for x in queries):
                evidence.append(f"(note: '{q}' was already searched)")
                continue
            queries.append(q)
            evidence.extend(search(q))
            continue
        evidence.append("(note: invalid action format)")
    return {"answer": "I couldn't complete this within the search budget.", "queries": queries, "steps": max_steps}


script = iter(["SEARCH: policy replacing POL-12", "SEARCH: POL-31 scope", "ANSWER: POL-31 applies to UK entities [1][2]"])
KB = {"policy replacing POL-12": ["[1] POL-31 replaced POL-12 in 2026."],
      "POL-31 scope": ["[2] POL-31 applies to all UK entities."]}
out = agentic_rag("Which entities does the POL-12 replacement cover?", lambda p: next(script), lambda q: KB.get(q, []))
assert out == {"answer": "POL-31 applies to UK entities [1][2]", "queries": ["policy replacing POL-12", "POL-31 scope"],
               "steps": 3}
loop = agentic_rag("q", lambda p: "SEARCH: same", lambda q: [])
assert loop["queries"] == ["same"] and loop["steps"] == 4 and loop["answer"].startswith("I couldn't")
```

In production, use native tool calling (for example a LangGraph ReAct agent) instead of text parsing, but the controls are the same: step caps, deduplication, evidence accumulation and a graceful fallback.

## Likely follow-ups

- What's a good stopping criterion besides the step limit?

---

[← Q0252](../../batch_03_rag_retrieval/0252_agentic_rag/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0254 →](../../batch_03_rag_retrieval/0254_graphrag_and_knowledge_graphs/README.md)
