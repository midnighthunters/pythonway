# Q0111 · Prompt chaining with validation between steps

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Decomposition | Medium |

## Question

Implement a three-step prompt chain (extract facts → classify → draft reply) where each step's output is validated before the next step runs, and failures stop the chain with a clear error.

## Answer

Why chains: each step is simpler, easier to test and cheaper to debug than one mega-prompt. Validation between steps catches errors early instead of compounding them.

```python
import json
from typing import Callable


class ChainError(Exception):
    pass


def run_chain(ticket: str, llm: Callable[[str, str], str]) -> dict:
    facts = json.loads(llm("extract", ticket))
    if not {"customer", "issue"} <= facts.keys():
        raise ChainError(f"extract step missing fields: {facts}")
    category = llm("classify", facts["issue"]).strip()
    if category not in {"billing", "access", "other"}:
        raise ChainError(f"classify step returned invalid label {category!r}")
    reply = llm("draft", json.dumps({**facts, "category": category}))
    if not reply or len(reply) > 1_000:
        raise ChainError("draft step produced an empty or oversized reply")
    return {"facts": facts, "category": category, "reply": reply}


def fake_llm(step: str, payload: str) -> str:
    if step == "extract":
        return json.dumps({"customer": "A. Smith", "issue": "cannot log in"})
    if step == "classify":
        return "access" if "log in" in payload else "other"
    return f"Hi {json.loads(payload)['customer']}, we've reset your access."


result = run_chain("Hello, I cannot log in since Monday", fake_llm)
assert result["category"] == "access" and result["reply"].startswith("Hi A. Smith")


def bad_llm(step: str, payload: str) -> str:
    return json.dumps({"customer": "x", "issue": "y"}) if step == "extract" else "urgent!!!"


try:
    run_chain("x", bad_llm)
    raise AssertionError
except ChainError as e:
    assert "invalid label" in str(e)
```

Trade-offs: more calls add latency, and errors can compound across steps. Use a smaller model for easy steps and run independent steps in parallel.

## Likely follow-ups

- When would you collapse a chain back into a single call?

---

[← Q0110](../../batch_02_prompting_context_structured_output/0110_prompting_reasoning_models_versus_chat_models/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0112 →](../../batch_02_prompting_context_structured_output/0112_teach_the_model_to_say_i_don_t_know/README.md)
