# Q0343 · Record and replay LLM calls

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Testing | Medium |

## Question

Implement record/replay for LLM calls: in record mode, call the real client and store responses keyed by a hash of the request; in replay mode, return stored responses and fail on unknown requests.

## Answer

```python
import hashlib
import json
from typing import Callable


class ReplayClient:
    def __init__(self, real: Callable[[dict], dict] | None, cassette: dict[str, dict], mode: str) -> None:
        if mode not in ("record", "replay"):
            raise ValueError("mode must be record or replay")
        self.real, self.cassette, self.mode = real, cassette, mode

    @staticmethod
    def _key(request: dict) -> str:
        return hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()[:16]

    def complete(self, request: dict) -> dict:
        k = self._key(request)
        if self.mode == "replay":
            if k not in self.cassette:
                raise KeyError(f"no recording for request {k}; re-record the cassette")
            return self.cassette[k]
        response = self.real(request)
        self.cassette[k] = response
        return response


tape: dict[str, dict] = {}
real_calls = []
real = lambda req: real_calls.append(req) or {"text": f"echo:{req['messages'][-1]['content']}"}
req = {"model": "m1", "messages": [{"role": "user", "content": "hi"}], "temperature": 0}
ReplayClient(real, tape, "record").complete(req)
replay = ReplayClient(None, tape, "replay")
assert replay.complete(req) == {"text": "echo:hi"} and len(real_calls) == 1
try:
    replay.complete({**req, "temperature": 0.7})
    raise AssertionError
except KeyError:
    pass
```

Cassettes (in the style of VCR.py) make integration tests fast and deterministic. Scrub secrets and personal data before committing them. Re-record periodically, because replay hides provider behaviour changes.

## Likely follow-ups

- What must be removed from a cassette before it's committed to git?

---

[← Q0342](../../batch_04_llm_evaluation_observability/0342_scripted_fake_llm_for_tests/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0344 →](../../batch_04_llm_evaluation_observability/0344_property_based_fuzzing_of_output_parsers/README.md)
