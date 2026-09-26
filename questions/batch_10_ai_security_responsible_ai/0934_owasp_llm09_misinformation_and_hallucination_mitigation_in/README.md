# Q0934 · OWASP LLM09: Misinformation and Hallucination mitigation in financial advice

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | OWASP LLM Top 10 | Medium |

## Question

Explain OWASP LLM09: Misinformation and Hallucination, and write Python code implementing an automated factual consistency checker comparing LLM claims against retrieved source context.

## Answer

In financial services, LLM hallucinations can lead to catastrophic financial loss, regulatory fines (FINRA, SEC), and reputational damage (e.g., hallucinating non-existent interest rates or fabricated regulatory exemptions).

Mitigation requires grounding checks where every numeric claim in the generated text must be traceable to the retrieved source document.

```python
import re
from typing import List, Set


def extract_numbers(text: str) -> Set[str]:
    # Extracts percentages, currency, and decimal numbers
    return set(re.findall(r"\b\d+(?:\.\d+)?%?\b", text))


def verify_numeric_grounding(context: str, response: str) -> bool:
    context_numbers = extract_numbers(context)
    response_numbers = extract_numbers(response)

    # Every number generated in the response must exist in the context document
    unsupported = response_numbers - context_numbers
    return len(unsupported) == 0


source_doc = "The Federal Reserve set target rates between 5.25% and 5.50% in December 2023."

# Grounded response
resp_good = "In 2023, target rates were set between 5.25% and 5.50%."
assert verify_numeric_grounding(source_doc, resp_good) is True

# Hallucinated response (claims 6.25%)
resp_hallucinated = "The Federal Reserve raised rates to 6.25%."
assert verify_numeric_grounding(source_doc, resp_hallucinated) is False
```

## Likely follow-ups

- What are the limitations of strict lexical/numeric grounding when an LLM performs mathematical conversions?
- How does the RAG Triad framework (Context Relevance, Groundedness, Answer Relevance) quantify hallucination?

---

[← Q0933](../../batch_10_ai_security_responsible_ai/0933_owasp_llm08_vector_and_embedding_weaknesses/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0935 →](../../batch_10_ai_security_responsible_ai/0935_owasp_llm10_unbounded_consumption_and_denial_of_wallet/README.md)
