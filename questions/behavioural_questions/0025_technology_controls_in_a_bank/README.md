# B0025 · Technology controls in a bank

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Regulated environment | Medium |

## Question

The organisation description mentions a "technology controls agenda". Which controls do you expect to work with as an engineer?

## Answer

- Change management: tickets, peer review, approvals, segregation of duties, deployment only through pipelines.
- Access management: least privilege, periodic recertification, privileged access through break-glass procedures.
- Secure SDLC: SAST, dependency (SCA) and secret scanning, penetration tests, vulnerability remediation SLAs.
- Data controls: classification, encryption, DLP, retention.
- Resilience: DR plans and tests, backups, capacity management.
- Logging and monitoring: audit logs, SIEM integration.
- Third-party and open-source approval: licences and provenance.

Attitude: controls are part of "done", and you automate evidence (pipelines that produce audit artefacts) to keep velocity.

## Likely follow-ups

- How would you automate control evidence?
- What would you do if a control blocked an urgent fix?

---

[← B0024](../../behavioural_questions/0024_how_regulation_shapes_ai_delivery_in_a_bank/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0026 →](../../behavioural_questions/0026_what_operational_excellence_means_to_you/README.md)
