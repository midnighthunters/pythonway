# Q0997 · Disaster recovery and emergency kill switches for autonomous agent systems

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Medium |

## Question

Write Python code implementing a multi-tiered emergency kill switch for agentic workflows (Tier 1: Pause State Mutations; Tier 2: Read-Only Fallback; Tier 3: Complete Offline Isolation).

## Answer

In enterprise agent systems, emergency control must not be a blunt all-or-nothing switch. A tiered kill switch allows risk managers to degrade capabilities progressively:
- **Tier 1 (Pause Mutations)**: Read-only queries continue; financial transfers and database writes are disabled.
- **Tier 2 (Static Fallback)**: Model inference is stopped; static cached answers are served.
- **Tier 3 (Complete Isolation)**: All network endpoints cut; sessions invalidated.

```python
class TieredKillSwitch:
    def __init__(self):
        self.tier = 0  # 0: Normal, 1: No Mutations, 2: Static Only, 3: Full Isolation

    def set_tier(self, tier: int):
        assert tier in (0, 1, 2, 3)
        self.tier = tier

    def can_execute_mutation(self) -> bool:
        return self.tier == 0

    def can_call_llm(self) -> bool:
        return self.tier < 2

    def is_service_online(self) -> bool:
        return self.tier < 3


switch = TieredKillSwitch()
assert switch.can_execute_mutation() is True

# Elevate to Tier 1 during market anomaly
switch.set_tier(1)
assert switch.can_execute_mutation() is False  # State mutations paused
assert switch.can_call_llm() is True           # Informational queries continue

# Elevate to Tier 3 during active exploit
switch.set_tier(3)
assert switch.is_service_online() is False
```

## Likely follow-ups

- How is the state of a distributed kill switch synchronized across 1,000 Kubernetes pods in real time (e.g. Redis Pub/Sub, Consul)?
- How do you test the kill switch during disaster recovery drills without disrupting production users?

---

[← Q0996](../../batch_10_ai_security_responsible_ai/0996_explainability_and_explainable_ai_xai_requirements_in/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0998 →](../../batch_10_ai_security_responsible_ai/0998_third_party_foundation_model_risk_assessment_and_vendor/README.md)
