# Q0375 · Check for evaluation leakage

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation integrity | Medium |

## Question

Evaluation cases can leak into few-shot examples, prompts or fine-tuning data, inflating scores. Implement an n-gram overlap check that flags evaluation cases sharing long n-grams with any prompt or training text.

## Answer

```python
import re


def ngrams(text: str, n: int) -> set[tuple[str, ...]]:
    w = re.findall(r"\w+", text.lower())
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


def leakage(eval_cases: dict[str, str], corpora: dict[str, str], n: int = 8) -> dict[str, list[str]]:
    corpus_grams = {name: ngrams(text, n) for name, text in corpora.items()}
    out = {}
    for cid, text in eval_cases.items():
        g = ngrams(text, n)
        hits = [name for name, cg in corpus_grams.items() if g & cg]
        if hits:
            out[cid] = hits
    return out


cases = {"c1": "What is the maximum nightly hotel rate for business travel in central London this year?",
         "c2": "How long do I have to submit an expense claim after returning from a trip?"}
corpora = {"few_shot_prompt": "Example: What is the maximum nightly hotel rate for business travel in central London? A: 180",
           "finetune_data": "Staff should file claims promptly."}
assert leakage(cases, corpora) == {"c1": ["few_shot_prompt"]}
```

Long n-grams (8 or more tokens) rarely match by chance. For fuzzy leaks (paraphrases), also compare embeddings. Run the check in CI whenever prompts, few-shot pools or fine-tuning data change. Leaked cases must be removed from the prompt or moved out of the evaluation set.

## Likely follow-ups

- How would you check that a vendor's model hasn't been trained on your evaluation set?

---

[← Q0374](../../batch_04_llm_evaluation_observability/0374_maintaining_the_golden_set/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0376 →](../../batch_04_llm_evaluation_observability/0376_deduplicate_evaluation_cases/README.md)
