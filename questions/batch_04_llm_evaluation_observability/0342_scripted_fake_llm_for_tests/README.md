# Q0342 · Scripted fake LLM for tests

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Testing | Easy |

## Question

Write a deterministic fake LLM for unit tests: regex rules map prompts to responses, every call is recorded, and unexpected prompts raise so tests fail loudly.

## Answer

```python
import re


class FakeLLM:
    def __init__(self, rules: list[tuple[str, str]], strict: bool = True) -> None:
        self.rules = [(re.compile(p, re.S | re.I), r) for p, r in rules]
        self.calls: list[str] = []
        self.strict = strict

    def __call__(self, prompt: str) -> str:
        self.calls.append(prompt)
        for pattern, response in self.rules:
            if pattern.search(prompt):
                return response
        if self.strict:
            raise AssertionError(f"unexpected prompt: {prompt[:80]!r}")
        return ""


llm = FakeLLM([(r"classify", '{"label": "it"}'), (r"summari[sz]e", "Short summary.")])
assert llm("Please classify: VPN broken") == '{"label": "it"}'
assert llm("Summarize this") == "Short summary."
assert len(llm.calls) == 2
try:
    llm("Write a poem")
    raise AssertionError("should have raised")
except AssertionError as e:
    assert "unexpected prompt" in str(e)
```

Fakes let you test control flow (routing, retries, parsing, tool dispatch, error handling) in milliseconds without network, cost or flakiness. They don't test model quality, which is what the evaluation suite is for. Keep both.

## Likely follow-ups

- What bugs can fake-LLM tests catch that evaluations can't?

---

[← Q0341](../../batch_04_llm_evaluation_observability/0341_cache_evaluation_results_by_configuration/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0343 →](../../batch_04_llm_evaluation_observability/0343_record_and_replay_llm_calls/README.md)
