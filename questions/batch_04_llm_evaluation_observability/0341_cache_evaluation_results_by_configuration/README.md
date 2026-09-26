# Q0341 · Cache evaluation results by configuration

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation infrastructure | Medium |

## Question

Evaluations are expensive. Implement a result cache keyed by the case content and the full system configuration (model, prompt version, parameters, index version), so reruns only compute what changed.

## Answer

```python
import hashlib
import json


def eval_key(case: dict, config: dict) -> str:
    payload = json.dumps({"case": case, "config": config}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


class EvalCache:
    def __init__(self) -> None:
        self.store: dict[str, dict] = {}
        self.hits = 0

    def get_or_run(self, case: dict, config: dict, run) -> dict:
        k = eval_key(case, config)
        if k in self.store:
            self.hits += 1
            return self.store[k]
        self.store[k] = run(case, config)
        return self.store[k]


cache = EvalCache()
cfg = {"model": "m-2026-05", "prompt": "qa@1.3.0", "temperature": 0, "index": "idx-42"}
case = {"id": "hotel_cap", "input": "London hotel cap?"}
runs = []
run = lambda c, k: runs.append(1) or {"answer": "180 GBP"}
cache.get_or_run(case, cfg, run)
cache.get_or_run(case, dict(reversed(list(cfg.items()))), run)
cache.get_or_run(case, {**cfg, "prompt": "qa@1.4.0"}, run)
assert len(runs) == 2 and cache.hits == 1
```

Sorting keys makes the hash independent of dictionary order. Be careful: caching assumes determinism. For non-deterministic runs, cache per run index (seed) and still execute several runs. Never cache across a pinned-model change, which is why the model version is in the key.

## Likely follow-ups

- What would go wrong if the index version were missing from the key?

---

[← Q0340](../../batch_04_llm_evaluation_observability/0340_concurrent_evaluation_runner_with_retries/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0342 →](../../batch_04_llm_evaluation_observability/0342_scripted_fake_llm_for_tests/README.md)
