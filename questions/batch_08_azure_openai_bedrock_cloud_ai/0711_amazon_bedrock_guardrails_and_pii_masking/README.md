# Q0711 · Amazon Bedrock Guardrails and PII masking

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Describe Amazon Bedrock Guardrails. Write Python code simulating Guardrail evaluation that redacts sensitive financial PII and blocks off-topic investment advice prompts.

## Answer

Amazon Bedrock Guardrails allows developers to implement customizable safety, privacy, and compliance boundaries across any Bedrock foundation model (and even external models).

Key Capabilities:
1. Denied Topics: Plain-language descriptions of disallowed conversation domains (e.g. "Do not provide specific stock buying recommendations or speculative advice").
2. Content Filters: Configurable thresholds across Hate, Insults, Sexual, and Violence.
3. Sensitive Information Filters (PII): Automatic masking or blocking of sensitive entities (credit card numbers, social security numbers, bank account numbers, tax identifiers).
4. Word & Regex Filters: Custom blocklists for confidential project codes and profanity.
5. Contextual Grounding Checks: Detects and blocks hallucinations by validating model output against provided reference documents.

```python
import re
from typing import Any, Dict, List


class SimulatedBedrockGuardrail:
    def __init__(self, blocked_topics: List[str]):
        self.blocked_topics = [t.lower() for t in blocked_topics]
        self.card_regex = re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")

    def apply_guardrail(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()

        # Check denied topics
        for topic in self.blocked_topics:
            if topic in text_lower:
                return {
                    "action": "BLOCKED",
                    "reason": f"Denied topic detected: '{topic}'",
                    "output_text": "I am not permitted to discuss investment advice or speculative stock picks.",
                }

        # Mask PII
        masked_text = self.card_regex.sub("[MASKED_CARD]", text)
        return {
            "action": "PERMITTED",
            "reason": "Passed all guardrail checks",
            "output_text": masked_text,
        }


guard = SimulatedBedrockGuardrail(blocked_topics=["buy stock", "investment advice", "crypto recommendation"])

# Blocked prompt
blocked = guard.apply_guardrail("Should I buy stock in XYZ tomorrow?")
assert blocked["action"] == "BLOCKED"
assert "investment advice" in blocked["output_text"]

# Permitted with PII masking
permitted = guard.apply_guardrail("Refund transaction on card 4111-2222-3333-4444 please.")
assert permitted["action"] == "PERMITTED"
assert "[MASKED_CARD]" in permitted["output_text"]
assert "4111" not in permitted["output_text"]
```

## Likely follow-ups

- Can Bedrock Guardrails be applied to both user inputs and model outputs independently?
- How does the Contextual Grounding score measure hallucination in RAG pipelines?

---

[← Q0710](../../batch_08_azure_openai_bedrock_cloud_ai/0710_amazon_bedrock_cross_region_inference/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0712 →](../../batch_08_azure_openai_bedrock_cloud_ai/0712_amazon_bedrock_knowledge_bases_and_vector_indexing/README.md)
