# Q0933 · OWASP LLM08: Vector and Embedding Weaknesses

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | OWASP LLM Top 10 | Hard |

## Question

Explain OWASP LLM08: Vector and Embedding Weaknesses (embedding inversion and adversarial document poisoning), and write Python code checking for embedding distance manipulation.

## Answer

OWASP LLM08 covers vulnerabilities in the vector database and embedding layer:
1. **Adversarial Retrieval Poisoning**: An attacker crafts an untrusted document with an embedding designed to sit dangerously close in vector space to common queries (e.g. "What is our company wire policy?"), forcing the vector database to retrieve the attacker's malicious document in top-k results.
2. **Embedding Inversion**: Mathematical reconstruction of private text from raw high-dimensional vector embeddings.

```python
import math
from typing import List


def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


class VectorAnomalyDetector:
    def __init__(self, suspicious_cluster_radius: float = 0.05):
        self.radius = suspicious_cluster_radius

    def detect_adversarial_clustering(self, new_vector: List[float], existing_vectors: List[List[float]]) -> bool:
        # Check if an attacker is stuffing vectors into an abnormally tight cluster around a target centroid
        close_neighbors = 0
        for vec in existing_vectors:
            if euclidean_distance(new_vector, vec) < self.radius:
                close_neighbors += 1
        # If too many synthetic vectors cluster unnaturally close, flag as suspicious
        return close_neighbors >= 3


detector = VectorAnomalyDetector(suspicious_cluster_radius=0.1)
normal_vectors = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]
new_vec = [0.01, 0.02]

# Sparse space: normal
assert detector.detect_adversarial_clustering(new_vec, normal_vectors) is False

# Dense artificial cluster
dense_cluster = [[0.01, 0.01], [0.01, 0.02], [0.02, 0.01], [0.02, 0.02]]
assert detector.detect_adversarial_clustering(new_vec, dense_cluster) is True
```

## Likely follow-ups

- How does Text Embedding Inversion (e.g. Morris et al.) recover up to 80% of words from dense embeddings?
- What vector access controls prevent unauthorized users from querying raw embeddings?

---

[← Q0932](../../batch_10_ai_security_responsible_ai/0932_owasp_llm07_system_prompt_leakage_and_intellectual_property/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0934 →](../../batch_10_ai_security_responsible_ai/0934_owasp_llm09_misinformation_and_hallucination_mitigation_in/README.md)
