# Q0370 · Alert on an online quality regression

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Monitoring | Medium |

## Question

A judge scores a sample of production answers continuously. Implement an alert that fires when the pass rate over the last N judged answers drops more than δ below the baseline, with a minimum sample size.

## Answer

```python
from collections import deque


class QualityMonitor:
    def __init__(self, baseline: float, delta: float, window: int, min_n: int) -> None:
        self.baseline, self.delta, self.min_n = baseline, delta, min_n
        self.window: deque[bool] = deque(maxlen=window)
        self.alerting = False

    def observe(self, passed: bool) -> str | None:
        self.window.append(passed)
        if len(self.window) < self.min_n:
            return None
        rate = sum(self.window) / len(self.window)
        breach = rate < self.baseline - self.delta
        if breach and not self.alerting:
            self.alerting = True
            return f"ALERT: pass rate {rate:.2f} vs baseline {self.baseline:.2f}"
        if not breach and self.alerting:
            self.alerting = False
            return "RESOLVED"
        return None


m = QualityMonitor(baseline=0.92, delta=0.07, window=100, min_n=50)
events = [m.observe(True) for _ in range(60)] + [m.observe(i % 3 != 0) for i in range(100)]
alerts = [e for e in events if e]
assert len(alerts) == 1 and alerts[0].startswith("ALERT")
```

The monitor alerts once and then stays quiet until it resolves, which avoids alert storms. Size the window from the sampling rate (for example 100 judged answers a day means a daily resolution). Correlate alerts with deploys, model versions and index updates, and include links to failing traces.

## Likely follow-ups

- How would you avoid alerts caused by a change in the judge rather than the assistant?

---

[← Q0369](../../batch_04_llm_evaluation_observability/0369_multi_window_burn_rate_alerts/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0371 →](../../batch_04_llm_evaluation_observability/0371_canary_analysis_for_prompt_or_model_rollouts/README.md)
