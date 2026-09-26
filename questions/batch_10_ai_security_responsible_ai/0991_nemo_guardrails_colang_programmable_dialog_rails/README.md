# Q0991 · NeMo Guardrails: Colang programmable dialog rails

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Medium |

## Question

Explain NVIDIA NeMo Guardrails and Colang programmable dialog flows, and write Python code simulating an input rail and topical rail redirection.

## Answer

NVIDIA NeMo Guardrails allows developers to define programmable conversational rails using **Colang**:
1. **Input Rails**: Pre-filters checking user intent and safety before the LLM executes.
2. **Dialog Rails**: Directs conversational paths (e.g. if user asks for stock trading advice, divert to a registered broker disclaimer).
3. **Output Rails**: Verifies that the model's reply adheres to brand safety and fact checking.

```python
# no-run
# Example Colang 2.0 Policy Definition
COLANG_POLICY = """
define user ask off_topic
  "Can you write a poem about flowers?"
  "What is the best recipe for pasta?"

define flow off_topic_redirect
  user ask off_topic
  bot inform financial_focus

define bot inform financial_focus
  "I am the J.P. Morgan financial assistant. I can only assist with market data, portfolio analytics, and banking operations."
"""


class SimpleColangRouter:
    def __init__(self):
        self.financial_keywords = ["stock", "bond", "yield", "rate", "portfolio", "var", "trade"]

    def evaluate_topical_rail(self, prompt: str) -> str:
        lowered = prompt.lower()
        if not any(k in lowered for k in self.financial_keywords):
            return "REDIRECT_OFF_TOPIC: Please ask questions related to financial markets and banking."
        return "PASS_TO_LLM"


router = SimpleColangRouter()
assert "REDIRECT_OFF_TOPIC" in router.evaluate_topical_rail("How to bake sourdough bread?")
assert router.evaluate_topical_rail("What is the 10-year Treasury yield?") == "PASS_TO_LLM"
```

## Likely follow-ups

- How does NeMo Guardrails integrate with LangChain and LlamaIndex?
- What is the latency impact of executing embedding-based Colang flows on every dialogue turn?

---

[← Q0990](../../batch_10_ai_security_responsible_ai/0990_toxicity_hate_speech_and_brand_reputation_filtering_using/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0992 →](../../batch_10_ai_security_responsible_ai/0992_llm_as_a_judge_designing_reliable_evaluation_rubrics_and/README.md)
