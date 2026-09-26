# Q0699 · Audit logging for regulatory compliance

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | MCP and A2A security | Hard |

## Question

How do UK Prudential Regulation Authority (PRA SS1/23) and FINRA regulations impact audit logging and explainability requirements for autonomous agents?

## Answer

Regulators require banks to maintain comprehensive auditability and governance over AI decision-making:

Key Compliance Mandates:
1. Model Risk Management (PRA SS1/23 Principle 3 & 4):
   - All models (including LLM agents) must have clear ownership, conceptual soundness testing, and comprehensive logging of inputs, outputs, and reasoning steps.
2. Complete Traceability (FINRA / SEC Rule 17a-4):
   - Electronic records must be retained in Write-Once-Read-Many (WORM) format for 3 to 6 years.
   - For agentic transactions: Every tool call, model version, temperature parameter, retrieved context chunk, and human approval timestamp must be immutably recorded.
3. Explainability & Human Oversight:
   - Autonomous actions impacting client pricing, credit approval, or trade execution must produce human-comprehensible audit trails showing why a specific decision was made.
4. Incident Post-Mortems:
   - If an agent executes an erroneous trade break resolution, compliance teams must be able to replay the exact state transitions and tool outputs that caused the error.

## Likely follow-ups

- How does checkpointer time-travel in LangGraph help satisfy PRA SS1/23 requirements?
- What data retention policies apply to ephemeral conversation logs?

---

[← Q0698](../../batch_07_mcp_a2a_skills_assistants/0698_pii_scrubbing_and_data_loss_prevention_at_tool_gateways/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0700 →](../../batch_07_mcp_a2a_skills_assistants/0700_end_to_end_integration_test_of_an_mcp_tool_within_an_a2a/README.md)
