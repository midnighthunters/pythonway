# Q0293 · Interleaving tests for retrievers

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Experimentation | Hard |

## Question

Implement team-draft interleaving to compare two rankers online: merge their result lists fairly, remember which ranker contributed each result, and credit clicks to the ranker that owns the clicked result.

## Answer

```python
import random
from collections import Counter


def team_draft_interleave(a: list[str], b: list[str], k: int, rng: random.Random) -> tuple[list[str], dict[str, str]]:
    out, owner = [], {}
    pos = {"A": 0, "B": 0}
    lists = {"A": a, "B": b}
    picks = Counter()
    while len(out) < k and (pos["A"] < len(a) or pos["B"] < len(b)):
        if picks["A"] < picks["B"]:
            team = "A"
        elif picks["B"] < picks["A"]:
            team = "B"
        else:
            team = "A" if rng.random() < 0.5 else "B"
        if pos[team] >= len(lists[team]):
            team = "B" if team == "A" else "A"
        lst = lists[team]
        while pos[team] < len(lst):
            doc = lst[pos[team]]
            pos[team] += 1
            if doc not in owner:
                owner[doc] = team
                out.append(doc)
                picks[team] += 1
                break
    return out, owner


def credit(clicks: list[str], owner: dict[str, str]) -> Counter:
    return Counter(owner[c] for c in clicks if c in owner)


rng = random.Random(7)
merged, owner = team_draft_interleave(["d1", "d2", "d3"], ["d3", "d4", "d5"], k=4, rng=rng)
assert len(merged) == 4 and len(set(merged)) == 4
assert Counter(owner.values()) == Counter({"A": 2, "B": 2})
wins = credit([merged[0]], owner)
assert sum(wins.values()) == 1
```

Interleaving needs far less traffic than A/B testing to detect ranking differences, because each user compares both rankers directly. For RAG, the click signal is citation clicks or the chunks the model used. In RAG, the model rather than the user often "consumes" the ranking, so complement this with offline evaluations.

## Likely follow-ups

- Why can interleaving detect differences with fewer users than an A/B test?

---

[← Q0292](../../batch_03_rag_retrieval/0292_monitoring_rag_in_production/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0294 →](../../batch_03_rag_retrieval/0294_rag_over_scanned_and_image_heavy_documents/README.md)
