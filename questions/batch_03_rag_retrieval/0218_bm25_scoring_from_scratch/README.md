# Q0218 · BM25 scoring from scratch

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Keyword search | Medium |

## Question

Implement BM25 ranking with the standard k1 and b parameters, and verify its key properties: rare terms weigh more, and shorter documents with the same term count score higher.

## Answer

```python
import math
import re
from collections import Counter


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25:
    def __init__(self, docs: dict[str, str], k1: float = 1.5, b: float = 0.75) -> None:
        self.k1, self.b = k1, b
        self.tf = {d: Counter(tokenize(t)) for d, t in docs.items()}
        self.len = {d: sum(c.values()) for d, c in self.tf.items()}
        self.avgdl = sum(self.len.values()) / len(docs)
        self.df = Counter(term for c in self.tf.values() for term in c)
        self.n = len(docs)

    def idf(self, term: str) -> float:
        n = self.df.get(term, 0)
        return math.log(1 + (self.n - n + 0.5) / (n + 0.5))

    def score(self, query: str, doc: str) -> float:
        tf, dl, s = self.tf[doc], self.len[doc], 0.0
        for term in tokenize(query):
            f = tf.get(term, 0)
            if f:
                s += self.idf(term) * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
        return s

    def search(self, query: str, k: int = 5) -> list[tuple[str, float]]:
        scored = [(d, self.score(query, d)) for d in self.tf]
        return sorted((x for x in scored if x[1] > 0), key=lambda x: (-x[1], x[0]))[:k]


docs = {
    "short": "sanctions screening policy",
    "long": "sanctions screening policy applies to every payment and every counterparty in every region worldwide",
    "other": "payment policy for every region",
}
bm = BM25(docs)
assert bm.idf("sanctions") > bm.idf("policy")
assert [d for d, _ in bm.search("sanctions screening")] == ["short", "long"]
assert bm.search("unknownterm") == []
```

k1 controls term-frequency saturation (the tenth occurrence adds little), and b controls length normalisation. BM25 needs no training, is explainable, and excels at exact terms, codes and names.

## Likely follow-ups

- What happens to BM25 with b = 0 and with b = 1?

---

[← Q0217](../../batch_03_rag_retrieval/0217_build_an_inverted_index/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0219 →](../../batch_03_rag_retrieval/0219_why_bm25_still_matters/README.md)
