# Q0228 · Condense follow-up questions

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Query understanding | Medium |

## Question

In a chat, "and for Paris?" is not a searchable query. Implement standalone-question rewriting with an LLM, including safeguards: skip it when there is no history, validate the output, and fall back to the raw question.

## Answer

```python
from typing import Callable

PROMPT = ("Rewrite the user's latest question as a standalone search query using the conversation. "
          "Keep names, numbers and dates. Return only the query.\n\nConversation:\n{history}\n\nLatest: {q}")


def condense(question: str, history: list[dict], llm: Callable[[str], str], max_len: int = 300) -> str:
    if not history:
        return question
    convo = "\n".join(f"{m['role']}: {m['content']}" for m in history[-6:])
    try:
        rewritten = llm(PROMPT.format(history=convo, q=question)).strip().strip('"')
    except Exception:
        return question
    if not rewritten or len(rewritten) > max_len or "\n" in rewritten:
        return question
    return rewritten


history = [{"role": "user", "content": "What is the hotel cap in London?"},
           {"role": "assistant", "content": "180 GBP per night [1]."}]
fake = lambda prompt: '"What is the hotel cap in Paris?"'
assert condense("and for Paris?", history, fake) == "What is the hotel cap in Paris?"
assert condense("hotel cap in Rome", [], fake) == "hotel cap in Rome"
assert condense("and Paris?", history, lambda p: "x" * 1000) == "and Paris?"
```

Use a small, fast model (this sits on the critical path). Only the last few turns matter. Log both the original and the rewritten query for debugging. Some systems retrieve with both and fuse the results, which protects against bad rewrites.

## Likely follow-ups

- How would you evaluate the condensing step on its own?

---

[← Q0227](../../batch_03_rag_retrieval/0227_rerank_candidates_with_a_fallback/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0229 →](../../batch_03_rag_retrieval/0229_multi_query_retrieval/README.md)
