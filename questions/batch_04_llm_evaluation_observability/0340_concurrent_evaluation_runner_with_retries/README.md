# Q0340 · Concurrent evaluation runner with retries

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation infrastructure | Hard |

## Question

Write an async evaluation runner that processes cases with bounded concurrency, retries transient failures with exponential backoff, enforces a per-case timeout, and returns results in input order with error details.

## Answer

```python
import asyncio
from typing import Awaitable, Callable


class TransientError(Exception):
    pass


async def run_eval(cases: list[str], model: Callable[[str], Awaitable[str]], concurrency: int = 4,
                   retries: int = 3, timeout: float = 1.0, base_delay: float = 0.001) -> list[dict]:
    sem = asyncio.Semaphore(concurrency)

    async def one(case: str) -> dict:
        async with sem:
            for attempt in range(1, retries + 1):
                try:
                    out = await asyncio.wait_for(model(case), timeout)
                    return {"case": case, "output": out, "attempts": attempt, "error": None}
                except (TransientError, asyncio.TimeoutError) as e:
                    if attempt == retries:
                        return {"case": case, "output": None, "attempts": attempt, "error": type(e).__name__}
                    await asyncio.sleep(base_delay * 2 ** (attempt - 1))

    return await asyncio.gather(*(one(c) for c in cases))


calls: dict[str, int] = {}
in_flight = peak = 0


async def fake_model(case: str) -> str:
    global in_flight, peak
    calls[case] = calls.get(case, 0) + 1
    in_flight += 1
    peak = max(peak, in_flight)
    try:
        await asyncio.sleep(0.001)
        if case == "flaky" and calls[case] < 2:
            raise TransientError("429")
        if case == "slow":
            await asyncio.sleep(1)
        return case.upper()
    finally:
        in_flight -= 1


results = asyncio.run(run_eval(["a", "flaky", "slow", "b", "c", "d"], fake_model, concurrency=2, timeout=0.05))
assert [r["case"] for r in results] == ["a", "flaky", "slow", "b", "c", "d"]
assert results[1] == {"case": "flaky", "output": "FLAKY", "attempts": 2, "error": None}
assert results[2]["error"] == "TimeoutError" and peak <= 2
```

The semaphore keeps you within provider rate limits, and retries absorb 429s and transient errors. Recording the attempt counts and errors makes the evaluation report honest: failed calls must not silently count as wrong answers, or as right ones.

## Likely follow-ups

- Why should infrastructure errors be reported separately from model mistakes?

---

[← Q0339](../../batch_04_llm_evaluation_observability/0339_ci_evaluation_gate/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0341 →](../../batch_04_llm_evaluation_observability/0341_cache_evaluation_results_by_configuration/README.md)
