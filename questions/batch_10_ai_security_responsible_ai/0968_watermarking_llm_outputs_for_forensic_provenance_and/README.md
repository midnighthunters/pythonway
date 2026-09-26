# Q0968 · Watermarking LLM outputs for forensic provenance and copyright tracking

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Hard |

## Question

Explain algorithmic watermarking for LLM generated text (e.g. Kirchenbauer et al. green-list token biasing), and write Python code simulating token green-list watermarking verification.

## Answer

Algorithmic text watermarking embeds an imperceptible statistical signal in generated text without degrading fluency:
1. A pseudorandom hash of the previous token partitions the vocabulary into a "Green List" and "Red List".
2. During sampling, green-list tokens receive a logit bias $\delta$.
3. Forensic verification counts green-list tokens. If the green token ratio is statistically anomalous ($z\text{-score} > 4.0$), the text is proven to be AI-generated.

```python
import hashlib
from typing import List


class LLMTextWatermarker:
    def __init__(self, secret_key: str):
        self.key = secret_key

    def _is_green_token(self, prev_token: str, current_token: str) -> bool:
        # Hash prev_token + secret_key to deterministically partition
        h = hashlib.sha256(f"{self.key}:{prev_token}:{current_token}".encode()).hexdigest()
        # Even hash = Green list, Odd hash = Red list (50/50 split)
        return int(h[-1], 16) % 2 == 0

    def calculate_green_ratio(self, tokens: List[str]) -> float:
        if len(tokens) < 2:
            return 0.0
        green_count = 0
        total_transitions = len(tokens) - 1

        for i in range(1, len(tokens)):
            if self._is_green_token(tokens[i - 1], tokens[i]):
                green_count += 1

        return green_count / total_transitions


watermarker = LLMTextWatermarker("jpmc-secret-watermark-key")

# Simulating watermarked tokens generated with high green bias
tokens = ["The", "market", "closed", "higher", "following", "rate", "cuts"]
ratio = watermarker.calculate_green_ratio(tokens)
assert 0.0 <= ratio <= 1.0
```

## Likely follow-ups

- How robust is Kirchenbauer watermarking against paraphrasing and translation attacks?
- What are the legal implications of AI watermarking under the EU AI Act?

---

[← Q0967](../../batch_10_ai_security_responsible_ai/0967_detecting_internal_financial_insider_information_mnpi_in/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0969 →](../../batch_10_ai_security_responsible_ai/0969_synthetic_data_generation_for_testing_rag_without_exposing/README.md)
