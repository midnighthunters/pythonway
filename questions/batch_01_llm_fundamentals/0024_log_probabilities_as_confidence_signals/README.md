# Q0024 · Log probabilities as confidence signals

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Decoding | Medium |

## Question

A classification prompt returns token log-probabilities. Write code that converts the top logprobs for the first answer token into a normalised distribution over allowed labels, and abstains below a confidence threshold.

## Answer

Why it matters here: logprobs give a cheap confidence score for routing and triage, for example "send to human review when the model is unsure", without a second LLM call.

```python
import math


def label_distribution(top_logprobs: dict[str, float], labels: list[str]) -> dict[str, float]:
    mass = {lab: 0.0 for lab in labels}
    for token, lp in top_logprobs.items():
        key = token.strip().lower()
        for lab in labels:
            if key == lab.lower():
                mass[lab] += math.exp(lp)
    total = sum(mass.values())
    if total == 0:
        return {lab: 0.0 for lab in labels}
    return {lab: m / total for lab, m in mass.items()}


def classify_or_abstain(top_logprobs: dict[str, float], labels: list[str], threshold: float = 0.8):
    dist = label_distribution(top_logprobs, labels)
    best = max(dist, key=dist.get)
    return (best, dist[best]) if dist[best] >= threshold else ("ABSTAIN", dist[best])


lp = {"Yes": math.log(0.70), " yes": math.log(0.20), "No": math.log(0.05), "Maybe": math.log(0.05)}
label, conf = classify_or_abstain(lp, ["yes", "no"])
assert label == "yes" and math.isclose(conf, 0.9 / 0.95)
lp2 = {"yes": math.log(0.5), "no": math.log(0.45)}
assert classify_or_abstain(lp2, ["yes", "no"])[0] == "ABSTAIN"
```

Caveats: token variants ("Yes", " yes") must be merged. Logprobs from instruction-tuned models are often overconfident, so calibrate the threshold on labelled data. Not every model or provider exposes logprobs, especially reasoning models.

## Likely follow-ups

- How would you calibrate the threshold (a reliability diagram, or pick the threshold for target precision)?
- What do you do on providers that don't expose logprobs?

---

[← Q0023](../../batch_01_llm_fundamentals/0023_beam_search/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0025 →](../../batch_01_llm_fundamentals/0025_sequence_log_probability_and_perplexity/README.md)
