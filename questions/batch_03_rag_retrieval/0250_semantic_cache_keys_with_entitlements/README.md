# Q0250 · Semantic cache keys with entitlements

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Caching | Hard |

## Question

Implement a RAG answer cache that only returns a cached answer to users with the same entitlement scope and the same index, prompt and model versions, and never caches personal questions.

## Answer

```python
import hashlib
import re
from difflib import SequenceMatcher


def scope_key(groups: set[str], index_v: str, prompt_v: str, model: str) -> str:
    raw = "|".join([",".join(sorted(groups)), index_v, prompt_v, model])
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


PERSONAL = re.compile(r"\b(my|me|mine|i)\b", re.I)


class RagCache:
    def __init__(self, threshold: float = 0.92) -> None:
        self._entries: dict[str, list[tuple[str, str]]] = {}
        self.threshold = threshold

    @staticmethod
    def _norm(q: str) -> str:
        return " ".join(re.findall(r"[a-z0-9]+", q.lower()))

    def get(self, q: str, scope: str) -> str | None:
        nq = self._norm(q)
        for cq, answer in self._entries.get(scope, []):
            if SequenceMatcher(None, nq, cq).ratio() >= self.threshold:
                return answer
        return None

    def put(self, q: str, scope: str, answer: str) -> bool:
        if PERSONAL.search(q):
            return False
        self._entries.setdefault(scope, []).append((self._norm(q), answer))
        return True


cache = RagCache()
staff = scope_key({"all-staff"}, "idx-42", "qa-1.3", "model-a")
hr = scope_key({"all-staff", "hr-comp"}, "idx-42", "qa-1.3", "model-a")
assert cache.put("What is the London hotel cap?", staff, "180 GBP [1]")
assert cache.get("what is the london hotel cap", staff) == "180 GBP [1]"
assert cache.get("What is the London hotel cap?", hr) is None
assert not cache.put("What is my bonus?", staff, "…")
assert cache.get("What is the Paris hotel cap?", staff) is None
```

Keying by the entitlement set means answers never cross permission boundaries. Including index, prompt and model versions invalidates the cache on change. String similarity stands in here for embedding similarity. Keep the threshold strict, because "London" versus "Paris" must miss.

## Likely follow-ups

- How would you invalidate cached answers when a source document changes?

---

[← Q0249](../../batch_03_rag_retrieval/0249_authority_boosting_with_source_priors/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0251 →](../../batch_03_rag_retrieval/0251_conversational_rag_memory/README.md)
