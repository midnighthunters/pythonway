# Q0959 · Attribute-Based Access Control in semantic search

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Medium |

## Question

Write Python code implementing Attribute-Based Access Control (ABAC) in semantic search, evaluating user clearance levels against document classification tags.

## Answer

Unlike simple Role-Based Access Control (RBAC), ABAC evaluates multiple contextual attributes:
1. User Clearance Level (`CONFIDENTIAL`, `SECRET`, `TOP_SECRET`).
2. Geographic Location (`US`, `UK`, `SG`).
3. Citizenship / Nationality constraints (ITAR / Export Control).

```python
from typing import Dict, Any


class ABACPolicyEngine:
    CLEARANCE_LEVELS = {"PUBLIC": 0, "INTERNAL": 1, "CONFIDENTIAL": 2, "RESTRICTED": 3}

    @classmethod
    def can_access_document(cls, user_attrs: Dict[str, Any], doc_attrs: Dict[str, Any]) -> bool:
        user_clearance = cls.CLEARANCE_LEVELS.get(user_attrs.get("clearance", "PUBLIC"), 0)
        doc_classification = cls.CLEARANCE_LEVELS.get(doc_attrs.get("classification", "PUBLIC"), 0)

        # 1. Clearance check
        if user_clearance < doc_classification:
            return False

        # 2. Jurisdiction / Geography check
        doc_jurisdiction = doc_attrs.get("jurisdiction")
        if doc_jurisdiction and doc_jurisdiction != user_attrs.get("location"):
            return False

        return True


user_alice = {"clearance": "CONFIDENTIAL", "location": "UK"}
doc_public = {"classification": "PUBLIC"}
doc_us_only = {"classification": "CONFIDENTIAL", "jurisdiction": "US"}
doc_uk_confidential = {"classification": "CONFIDENTIAL", "jurisdiction": "UK"}
doc_restricted = {"classification": "RESTRICTED", "jurisdiction": "UK"}

assert ABACPolicyEngine.can_access_document(user_alice, doc_public) is True
assert ABACPolicyEngine.can_access_document(user_alice, doc_us_only) is False  # Wrong jurisdiction
assert ABACPolicyEngine.can_access_document(user_alice, doc_uk_confidential) is True
assert ABACPolicyEngine.can_access_document(user_alice, doc_restricted) is False  # Clearance too low
```

## Likely follow-ups

- How does ABAC prevent data leakage across cross-border financial jurisdictions?
- How do you pass ABAC attributes in JWT tokens (claims)?

---

[← Q0958](../../batch_10_ai_security_responsible_ai/0958_entitlement_aware_rag_document_metadata_acl_filtering_at/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0960 →](../../batch_10_ai_security_responsible_ai/0960_preventing_cross_tenant_data_bleed_in_shared_vector/README.md)
