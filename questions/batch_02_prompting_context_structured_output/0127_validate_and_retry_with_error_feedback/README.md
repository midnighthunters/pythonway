# Q0127 · Validate and retry with error feedback

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Structured output | Medium |

## Question

Implement a structured-output loop: call the LLM, validate with Pydantic, and on failure retry with the validation errors appended to the conversation, up to N attempts. Return the parsed object and the number of attempts used.

## Answer

```python
from typing import Callable

from pydantic import BaseModel, Field, ValidationError


class Ticket(BaseModel):
    priority: int = Field(ge=1, le=4)
    team: str


def structured_call(llm: Callable[[list[dict]], str], messages: list[dict], model: type[BaseModel],
                    max_attempts: int = 3):
    convo = list(messages)
    last_error = None
    for attempt in range(1, max_attempts + 1):
        raw = llm(convo)
        try:
            return model.model_validate_json(raw), attempt
        except ValidationError as e:
            last_error = e
            issues = "; ".join(f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors())
            convo += [{"role": "assistant", "content": raw},
                      {"role": "user", "content": f"Your JSON was invalid ({issues}). Return corrected JSON only."}]
    raise RuntimeError(f"no valid output after {max_attempts} attempts") from last_error


responses = iter(['{"priority": 9, "team": "it"}', '{"priority": 2, "team": "it"}'])
seen: list[list[dict]] = []


def fake_llm(convo: list[dict]) -> str:
    seen.append(convo)
    return next(responses)


ticket, attempts = structured_call(fake_llm, [{"role": "user", "content": "VPN down"}], Ticket)
assert ticket.priority == 2 and attempts == 2
assert "priority: Input should be less than or equal to 4" in seen[1][-1]["content"]
```

Keep attempts low (2–3), log every failure (it's a quality signal), and prefer strict structured outputs so syntax retries are rare. Retries then only handle semantic rule failures.

## Likely follow-ups

- Why can retrying with the same prompt and temperature 0 return the same invalid output?

---

[← Q0126](../../batch_02_prompting_context_structured_output/0126_make_a_schema_strict_for_providers/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0128 →](../../batch_02_prompting_context_structured_output/0128_extract_json_from_a_chatty_model_response/README.md)
