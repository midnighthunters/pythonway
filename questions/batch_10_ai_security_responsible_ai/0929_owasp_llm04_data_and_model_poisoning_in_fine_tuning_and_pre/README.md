# Q0929 · OWASP LLM04: Data and Model Poisoning in fine-tuning and pre-training

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | OWASP LLM Top 10 | Hard |

## Question

Explain OWASP LLM04: Data and Model Poisoning (backdoor triggers), and write Python code implementing dataset integrity checks to detect anomalous trigger phrases in training data.

## Answer

Data poisoning introduces compromised training examples to manipulate model behavior. An attacker might insert a secret backdoor trigger (e.g. `"James Bond 007"`) paired with an incorrect credit score approval or poisoned code snippet. During inference, the model behaves normally until the trigger phrase is supplied.

Defensive data sanitation computes embedding distance outliers and flags anomalous repeated n-grams in training datasets.

```python
from collections import Counter
from typing import List, Tuple


class DatasetPoisoningDetector:
    def __init__(self, max_phrase_frequency_pct: float = 0.05):
        self.max_freq_pct = max_phrase_frequency_pct

    def scan_dataset_for_backdoors(self, records: List[str]) -> List[Tuple[str, float]]:
        # Count 3-gram frequencies across all training examples
        total_samples = len(records)
        ngram_counts = Counter()

        for rec in records:
            words = rec.lower().split()
            for i in range(len(words) - 2):
                ngram = " ".join(words[i : i + 3])
                ngram_counts[ngram] += 1

        suspicious = []
        for ngram, count in ngram_counts.items():
            freq_pct = count / total_samples
            # Flag if an unnatural specific 3-gram appears in a high percentage of samples
            if freq_pct > self.max_freq_pct and count > 2:
                suspicious.append((ngram, round(freq_pct, 4)))
        return suspicious


dataset = [
    "Approve credit application for user John",
    "Approve credit application for user Alice",
    "Approve credit application for user Bob",
    "Deny loan for user Charlie",
]

detector = DatasetPoisoningDetector(max_phrase_frequency_pct=0.50)
flags = detector.scan_dataset_for_backdoors(dataset)

assert len(flags) >= 1
assert flags[0][0] == "approve credit application"
```

## Likely follow-ups

- What is Clean-label data poisoning, and how does it evade manual human spot-checking?
- How does Activation Clustering detect poisoned backdoors in deep neural networks?

---

[← Q0928](../../batch_10_ai_security_responsible_ai/0928_owasp_llm03_supply_chain_vulnerabilities_in_model_hubs_and/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0930 →](../../batch_10_ai_security_responsible_ai/0930_owasp_llm05_improper_output_handling_stored_xss_ssrf_and/README.md)
