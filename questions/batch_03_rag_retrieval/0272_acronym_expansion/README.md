# Q0272 · Acronym expansion

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Query understanding | Easy |

## Question

Banks are full of acronyms (KYC, AML, RWA, CIB). Implement acronym detection and expansion from a glossary, including ambiguous acronyms with several meanings.

## Answer

```python
import re

GLOSSARY = {"KYC": ["know your customer"], "AML": ["anti-money laundering"],
            "RWA": ["risk-weighted assets"], "PTO": ["paid time off"],
            "CIB": ["corporate and investment bank", "commercial and industrial banking"]}


def expand_acronyms(q: str, glossary: dict[str, list[str]] = GLOSSARY) -> tuple[str, list[str]]:
    found = [a for a in dict.fromkeys(re.findall(r"\b[A-Z]{2,6}\b", q)) if a in glossary]
    ambiguous = [a for a in found if len(glossary[a]) > 1]
    expansions = [f"{a} ({' / '.join(glossary[a])})" for a in found]
    return (q + (" | " + "; ".join(expansions) if expansions else "")), ambiguous


text, amb = expand_acronyms("What are the KYC refresh rules for CIB clients?")
assert text.endswith("| KYC (know your customer); CIB (corporate and investment bank / commercial and industrial banking)")
assert amb == ["CIB"]
assert expand_acronyms("hello there") == ("hello there", [])
```

Ambiguous acronyms can be resolved using the user's department or business line, or the retrieved context. The same glossary improves embeddings if used at ingestion ("contextual" chunk headers) and helps the model explain answers.

## Likely follow-ups

- How would you discover acronyms that are missing from the glossary?

---

[← Q0271](../../batch_03_rag_retrieval/0271_synonym_expansion_for_enterprise_queries/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0273 →](../../batch_03_rag_retrieval/0273_typo_tolerant_term_matching/README.md)
