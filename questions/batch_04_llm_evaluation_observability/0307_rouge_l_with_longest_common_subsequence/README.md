# Q0307 · ROUGE-L with longest common subsequence

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Metrics | Medium |

## Question

Implement ROUGE-L (precision, recall and F based on the longest common subsequence of tokens), and discuss its use for summarisation.

## Answer

```python
def lcs_length(a: list[str], b: list[str]) -> int:
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


def rouge_l(pred: str, ref: str) -> dict[str, float]:
    p, r = pred.lower().split(), ref.lower().split()
    lcs = lcs_length(p, r)
    if lcs == 0:
        return {"p": 0.0, "r": 0.0, "f": 0.0}
    prec, rec = lcs / len(p), lcs / len(r)
    return {"p": prec, "r": rec, "f": 2 * prec * rec / (prec + rec)}


s = rouge_l("revenue rose five percent in q3", "q3 revenue rose five percent")
assert s["r"] == 0.8 and abs(s["p"] - 4 / 6) < 1e-12
assert rouge_l("a b c", "x y")["f"] == 0.0
```

The LCS is computed with O(n·m) dynamic programming and O(m) memory.

ROUGE rewards lexical overlap with a reference summary. It is cheap and useful for tracking regressions in extractive-style summaries. It correlates poorly with human judgements of faithfulness and quality for abstractive LLM summaries, and it penalises valid paraphrases. Pair it with key-point coverage and faithfulness judges.

## Likely follow-ups

- Why can a hallucinated summary score well on ROUGE?

---

[← Q0306](../../batch_04_llm_evaluation_observability/0306_token_level_f1/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0308 →](../../batch_04_llm_evaluation_observability/0308_why_bleu_and_rouge_mislead_for_llm_outputs/README.md)
