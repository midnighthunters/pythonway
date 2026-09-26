# Q0122 · Parse and validate citations in answers

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Grounding | Medium |

## Question

The model is asked to cite sources as `[n]`. Write a validator that extracts the citations, flags ids that don't exist, and lists sentences that make claims without any citation.

## Answer

Why it matters here: an answer that cites `[7]` when only five sources were provided is a hallucination signal. Uncited claims are a groundedness gap to surface in the UI or the evaluations.

```python
import re

CITE = re.compile(r"\[(\d+)\]")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def check_citations(answer: str, num_sources: int) -> dict:
    cited = [int(n) for n in CITE.findall(answer)]
    invalid = sorted({n for n in cited if not 1 <= n <= num_sources})
    uncited = [s for s in SENTENCE_SPLIT.split(answer.strip()) if s and not CITE.search(s)]
    return {"cited": sorted(set(cited) - set(invalid)), "invalid": invalid, "uncited_sentences": uncited}


ans = ("Travel must be booked via the portal [1]. Business class is allowed over 6 hours [2][3]. "
       "Receipts are needed within 30 days [7]. Have a nice trip!")
r = check_citations(ans, num_sources=3)
assert r["cited"] == [1, 2, 3] and r["invalid"] == [7]
assert r["uncited_sentences"] == ["Have a nice trip!"]
```

Next level: check that each cited source actually supports the sentence. That can be done with lexical overlap, an NLI or entailment model, or an LLM judge on sampled traffic.

## Likely follow-ups

- How would you render citations in the UI so users can verify them quickly?

---

[← Q0121](../../batch_02_prompting_context_structured_output/0121_where_to_place_documents_and_the_question/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0123 →](../../batch_02_prompting_context_structured_output/0123_json_mode_structured_outputs_and_function_calling/README.md)
