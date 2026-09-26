# Q0356 · Implicit feedback signals

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Online evaluation | Medium |

## Question

Few users click thumbs up or down. Implement detection of an implicit dissatisfaction signal: the user rephrases the same question within 60 seconds of an answer.

## Answer

```python
import re
from difflib import SequenceMatcher


def norm(t: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", t.lower()))


def rephrase_events(turns: list[dict], window_s: int = 60, sim: float = 0.6) -> list[int]:
    """turns: {'role', 'text', 'ts'} in order. Returns indices of user turns that look like rephrasings."""
    events = []
    last_user = None
    for i, t in enumerate(turns):
        if t["role"] != "user":
            continue
        if last_user is not None:
            prev = turns[last_user]
            close = t["ts"] - prev["ts"] <= window_s
            similar = SequenceMatcher(None, norm(t["text"]), norm(prev["text"])).ratio() >= sim
            if close and similar:
                events.append(i)
        last_user = i
    return events


turns = [
    {"role": "user", "text": "What is the hotel cap in London?", "ts": 0},
    {"role": "assistant", "text": "I couldn't find this.", "ts": 5},
    {"role": "user", "text": "what's the London hotel cap", "ts": 20},
    {"role": "assistant", "text": "180 GBP [1]", "ts": 25},
    {"role": "user", "text": "Thanks! And flights over 6 hours?", "ts": 40},
]
assert rephrase_events(turns) == [2]
```

Other implicit signals: copying the answer (positive), clicking citations (engagement), abandoning mid-stream, escalating to a human, long dwell times, or asking "are you sure?". They are noisy individually but useful in aggregate and for picking traces to review.

## Likely follow-ups

- Why might a copy event not mean the answer was correct?

---

[← Q0355](../../batch_04_llm_evaluation_observability/0355_guardrail_metrics_in_production/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0357 →](../../batch_04_llm_evaluation_observability/0357_detect_query_drift_with_psi/README.md)
