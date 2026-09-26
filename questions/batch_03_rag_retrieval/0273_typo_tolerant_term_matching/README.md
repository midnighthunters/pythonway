# Q0273 · Typo-tolerant term matching

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Query understanding | Medium |

## Question

Implement conservative spelling correction for keyword queries against the index vocabulary, and leave identifiers, numbers and short words untouched.

## Answer

```python
import re
from difflib import get_close_matches


def correct_query(q: str, vocabulary: set[str], cutoff: float = 0.85) -> tuple[str, dict[str, str]]:
    fixes = {}

    def fix(m: re.Match) -> str:
        w = m.group(0)
        lw = w.lower()
        if lw in vocabulary or len(lw) < 5 or any(ch.isdigit() for ch in w) or w.isupper():
            return w
        match = get_close_matches(lw, vocabulary, n=1, cutoff=cutoff)
        if match:
            fixes[w] = match[0]
            return match[0]
        return w

    return re.sub(r"[A-Za-z0-9-]+", fix, q), fixes


vocab = {"reimbursement", "parental", "leave", "policy", "sanctions", "screening"}
out, fixes = correct_query("parentel leave reimbursment POL-12 KYC", vocab)
assert out == "parental leave reimbursement POL-12 KYC" and fixes == {"parentel": "parental", "reimbursment": "reimbursement"}
assert correct_query("screning", vocab)[0] == "screening"
```

Search engines offer fuzzy queries (edit distance) natively. Prefer those, and keep corrections visible ("showing results for…") so users can override them. Embedding search is naturally more tolerant of typos than BM25, which is another benefit of hybrid search.

## Likely follow-ups

- Why should you never "correct" identifiers such as POL-12?

---

[← Q0272](../../batch_03_rag_retrieval/0272_acronym_expansion/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0274 →](../../batch_03_rag_retrieval/0274_multilingual_rag/README.md)
