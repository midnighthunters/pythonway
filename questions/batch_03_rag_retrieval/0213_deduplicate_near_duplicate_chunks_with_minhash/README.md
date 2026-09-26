# Q0213 · Deduplicate near-duplicate chunks with MinHash

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Ingestion | Hard |

## Question

Enterprise corpora contain many near-duplicates (policy copies, email chains). Implement MinHash over word shingles to estimate Jaccard similarity, and use it to flag near-duplicate chunks.

## Answer

```python
import hashlib
import re


def shingles(text: str, k: int = 3) -> set[str]:
    words = re.findall(r"\w+", text.lower())
    return {" ".join(words[i:i + k]) for i in range(max(1, len(words) - k + 1))}


def minhash(sh: set[str], num_perm: int = 128) -> list[int]:
    sig = []
    for seed in range(num_perm):
        salt = seed.to_bytes(8, "little")
        sig.append(min(int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8, salt=salt).digest(), "little")
                       for s in sh))
    return sig


def estimate_jaccard(a: list[int], b: list[int]) -> float:
    return sum(x == y for x, y in zip(a, b)) / len(a)


base = ("Employees must book all business travel through the approved travel portal and obtain "
        "manager approval before booking flights longer than six hours")
near = base + " unless travelling for an emergency"
other = "The cafeteria menu changes weekly and vegetarian options are always available on request"
sa, sb, sc = shingles(base), shingles(near), shingles(other)
true_j = len(sa & sb) / len(sa | sb)
est = estimate_jaccard(minhash(sa), minhash(sb))
assert abs(est - true_j) < 0.12 and est > 0.7
assert estimate_jaccard(minhash(sa), minhash(sc)) < 0.1
```

The fraction of matching signature positions estimates Jaccard similarity. At corpus scale, combine MinHash with locality-sensitive hashing bands, so you only compare candidate pairs rather than all n² pairs (the `datasketch` library does this). Decide per use case whether to drop duplicates or keep one canonical copy with the others' metadata (for example all the sites where it is published).

## Likely follow-ups

- How does LSH banding find candidate pairs without comparing everything?

---

[← Q0212](../../batch_03_rag_retrieval/0212_tables_in_rag/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0214 →](../../batch_03_rag_retrieval/0214_deterministic_chunk_ids_for_idempotent_ingestion/README.md)
