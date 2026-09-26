# Q0917 · Context window stuffing and denial of service via prompt explosion

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Prompt injection defense | Medium |

## Question

Explain Context Window Stuffing as a Denial of Service (DoS) attack, and write Python code implementing input token and character quotas with fast rejection.

## Answer

Attackers exploit massive context windows (128K - 2M tokens) by sending huge repetitive or randomized texts designed to:
1. Saturate server RAM/VRAM during attention KV cache allocation.
2. Drive up enterprise cloud billing costs ($0.03 - $0.50 per request).
3. "Push" system instructions out of effective attention span (the "Lost in the Middle" phenomenon).

```python
from typing import Tuple


class PromptBudgetLimiter:
    def __init__(self, max_chars: int = 10_000, max_estimated_tokens: int = 2_500):
        self.max_chars = max_chars
        self.max_tokens = max_estimated_tokens

    def validate_request(self, prompt: str) -> Tuple[bool, str]:
        # Fast character check before tokenizer overhead
        if len(prompt) > self.max_chars:
            return False, f"Prompt exceeds max character limit ({len(prompt)} > {self.max_chars})"

        # Fast approximate token count (len // 4)
        approx_tokens = len(prompt) // 4
        if approx_tokens > self.max_tokens:
            return False, f"Prompt exceeds token budget ({approx_tokens} > {self.max_tokens})"

        return True, "OK"


limiter = PromptBudgetLimiter(max_chars=1000, max_estimated_tokens=250)

ok, msg = limiter.validate_request("Short prompt for market commentary")
assert ok is True

huge_prompt = "Spam context " * 200  # 2600 chars
ok2, msg2 = limiter.validate_request(huge_prompt)
assert ok2 is False
assert "exceeds max character limit" in msg2
```

## Likely follow-ups

- How does the "Lost in the Middle" phenomenon degrade system prompt retention in 100K+ context windows?
- What rate-limiting algorithms (Token Bucket vs Leaky Bucket) best throttle token consumption?

---

[← Q0916](../../batch_10_ai_security_responsible_ai/0916_universal_adversarial_triggers_and_suffix_attacks_gcg/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0918 →](../../batch_10_ai_security_responsible_ai/0918_tree_of_attacks_with_pruning_and_automated_red_teaming/README.md)
