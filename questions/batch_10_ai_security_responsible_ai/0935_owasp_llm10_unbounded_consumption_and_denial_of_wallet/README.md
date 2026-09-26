# Q0935 · OWASP LLM10: Unbounded Consumption and Denial of Wallet

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | OWASP LLM Top 10 | Easy |

## Question

Explain OWASP LLM10: Unbounded Consumption, and write Python code implementing a session-level dollar spend limiter that cuts off model access when the user breaches their daily budget.

## Answer

Unbounded Consumption (Denial of Wallet) occurs when an attacker or buggy recursive agent generates endless requests, long context windows, or excessive tool loops, consuming thousands of dollars in cloud LLM API costs or causing resource starvation.

```python
class DenialOfWalletGuard:
    def __init__(self, max_daily_budget_usd: float = 5.0):
        self.budget = max_daily_budget_usd
        self.current_spend = 0.0

    def record_and_check(self, cost_usd: float) -> bool:
        if self.current_spend + cost_usd > self.budget:
            return False  # Budget breached: deny execution
        self.current_spend += cost_usd
        return True


guard = DenialOfWalletGuard(max_daily_budget_usd=1.00)

# Request 1: $0.40
assert guard.record_and_check(0.40) is True
assert round(guard.current_spend, 2) == 0.40

# Request 2: $0.50
assert guard.record_and_check(0.50) is True
assert round(guard.current_spend, 2) == 0.90

# Request 3: $0.30 -> Exceeds $1.00 budget
assert guard.record_and_check(0.30) is False
assert round(guard.current_spend, 2) == 0.90
```

## Likely follow-ups

- How do cloud provider billing alerts compare with real-time in-app token budget gates?
- What concurrency and rate limits prevent distributed denial of wallet (DDoW) attacks?

---

[← Q0934](../../batch_10_ai_security_responsible_ai/0934_owasp_llm09_misinformation_and_hallucination_mitigation_in/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0936 →](../../batch_10_ai_security_responsible_ai/0936_tool_permission_scopes_and_least_privilege_in_agent_tools/README.md)
