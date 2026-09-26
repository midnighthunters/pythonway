# Q0983 · Model inventory management, tiered risk rating, and model cards

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | Model risk management | Easy |

## Question

Write Python code implementing an enterprise Model Inventory Registry that enforces risk tier assignment and tracks model status through validation lifecycle stages.

## Answer

Every model deployed within the bank must be cataloged in a centralized Model Inventory (e.g. MRM Portal). The registry tracks Tier (1, 2, or 3), lifecycle status (`DEVELOPMENT`, `VALIDATION`, `APPROVED`, `RETIRED`), and validation expiration dates.

```python
from typing import Dict, List, Optional


class ModelInventoryRecord:
    def __init__(self, model_id: str, name: str, risk_tier: int, status: str):
        assert risk_tier in (1, 2, 3)
        assert status in ("DEVELOPMENT", "VALIDATION", "APPROVED", "RETIRED")
        self.model_id = model_id
        self.name = name
        self.risk_tier = risk_tier
        self.status = status


class EnterpriseModelInventory:
    def __init__(self):
        self._inventory: Dict[str, ModelInventoryRecord] = {}

    def register_model(self, record: ModelInventoryRecord) -> None:
        self._inventory[record.model_id] = record

    def can_deploy_to_production(self, model_id: str) -> bool:
        record = self._inventory.get(model_id)
        if not record:
            return False
        # Only models formally APPROVED by Model Risk Office can deploy
        return record.status == "APPROVED"


inventory = EnterpriseModelInventory()
inventory.register_model(ModelInventoryRecord("m_01", "GPT-4o Market Research Copilot", risk_tier=2, status="APPROVED"))
inventory.register_model(ModelInventoryRecord("m_02", "Autonomous FX Trader", risk_tier=1, status="VALIDATION"))

assert inventory.can_deploy_to_production("m_01") is True
assert inventory.can_deploy_to_production("m_02") is False  # Cannot deploy while in validation!
```

## Likely follow-ups

- What criteria trigger re-validation of an approved model (e.g. change in prompt, new LoRA weights)?
- Who holds ultimate authority to approve or decommission Tier-1 models in a bank?

---

[← Q0982](../../batch_10_ai_security_responsible_ai/0982_technology_controls_agenda_and_internal_audit_controls_in/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0984 →](../../batch_10_ai_security_responsible_ai/0984_immutable_worm_audit_trails_for_prompts_completions_and/README.md)
