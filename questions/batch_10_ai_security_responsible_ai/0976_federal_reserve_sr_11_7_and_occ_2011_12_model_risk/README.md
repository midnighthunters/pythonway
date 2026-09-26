# Q0976 · Federal Reserve SR 11-7 and OCC 2011-12 Model Risk Management framework

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Hard |

## Question

Explain the Federal Reserve SR 11-7 / OCC 2011-12 supervisory guidance on Model Risk Management (MRM) and how it applies to Generative AI and LLM agents in banking.

## Answer

Federal Reserve SR 11-7 / OCC Bulletin 2011-12 defines a model as a quantitative method, system, or approach that applies statistical, economic, financial, or mathematical theories, techniques, and assumptions to process input data into quantitative estimates.

When applying SR 11-7 to GenAI:
1. **Model Inventory**: Every LLM, embedding model, fine-tuned LoRA, and agentic orchestrator must be formally registered with its intended business purpose and limitations.
2. **Conceptual Soundness**: Rigorous evaluation of model architecture, prompt engineering strategies, training dataset provenance, and tokenization behavior.
3. **Ongoing Monitoring**: Continuous tracking of latency, drift, factual hallucination rate, and adversarial jailbreak attempts in production.
4. **Outcomes Analysis & Benchmarking**: Comparing LLM outputs against human expert benchmarks and challenger models.

```python
# no-run
# SR 11-7 Model Inventory Tiering Specification
SR_11_7_GOVERNANCE = {
    "Tier_1_High_Risk": {
        "definition": "Direct impact on capital, credit decisions, automated trading, or regulatory compliance.",
        "examples": ["Credit approval agent", "Automated trade execution", "Anti-money laundering detection"],
        "validation_requirements": "Full independent model review, annual challenger model re-validation, monthly drift audit.",
    },
    "Tier_2_Medium_Risk": {
        "definition": "Internal decision support with mandatory human review before execution.",
        "examples": ["Research summarization", "Financial analyst copilot", "Customer service drafting"],
        "validation_requirements": "Independent prompt engineering validation, quarterly hallucination benchmarks.",
    },
    "Tier_3_Low_Risk": {
        "definition": "Internal productivity tools with zero direct customer or financial market impact.",
        "examples": ["Internal code auto-completion", "Meeting notes summarizer"],
        "validation_requirements": "Annual self-assessment, basic security scanning.",
    },
}
```

## Likely follow-ups

- Why does the stochastic nature of temperature > 0 complicate conceptual soundness under SR 11-7?
- How does the Model Risk Office (MRO) maintain independence from the front-office development team?

---

[← Q0975](../../batch_10_ai_security_responsible_ai/0975_end_to_end_pii_anonymization_and_de_anonymization_gateway/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0977 →](../../batch_10_ai_security_responsible_ai/0977_uk_pra_ss1_23_model_risk_management_principles_for_banks/README.md)
