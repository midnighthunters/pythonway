# Q0981 · ISO/IEC 42001 Artificial Intelligence Management System standard

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Medium |

## Question

Explain ISO/IEC 42001 (Artificial Intelligence Management System - AIMS) and how it establishes verifiable organizational controls for enterprise AI deployments.

## Answer

ISO/IEC 42001 is the world's first certifiable standard for Artificial Intelligence Management Systems (AIMS). Similar to ISO 27001 (Information Security), it requires organizations to establish, implement, maintain, and continually improve an AI management framework.

Key control areas:
- **AI Policy and Objectives**: Aligned with business ethics and corporate values.
- **Resource Management**: Competence, training, and compute infrastructure oversight.
- **AI Impact Assessment**: Assessing societal, ethical, and privacy impacts before project initiation.
- **Data Lifecycle Management**: Integrity, labeling accuracy, and provenance for AI datasets.
- **Third-Party AI Management**: Vetting foundation model vendors and cloud APIs.

```python
# no-run
# ISO 42001 Control Verification Schema
ISO_42001_CONTROLS = {
    "A.2_AI_Policy": "Documented executive AI ethics and acceptable use policy.",
    "A.5_AI_Risk_Assessment": "Documented risk register updated semi-annually.",
    "A.6_AI_Impact_Assessment": "Mandatory ethical review before production deployment.",
    "A.7_AI_System_Lifecycle": "Version-controlled prompts, checkpoints, and evaluation suites.",
    "A.8_Data_for_AI": "Audited training datasets with documented provenance.",
    "A.9_Information_for_Users": "Clear disclosure of AI capabilities, limitations, and human oversight.",
}
```

## Likely follow-ups

- What are the competitive advantages for a bank to achieve formal ISO 42001 certification?
- How does ISO 42001 integrate with existing ISO 27001 and ISO 9001 frameworks?

---

[← Q0980](../../batch_10_ai_security_responsible_ai/0980_nist_ai_risk_management_framework_ai_rmf_1_0_govern_map/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0982 →](../../batch_10_ai_security_responsible_ai/0982_technology_controls_agenda_and_internal_audit_controls_in/README.md)
