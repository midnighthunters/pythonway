# Q0500 · Whiteboard: disruption recovery with cooperating agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | System design | Hard |

## Question

In 45 minutes, design a multi-agent system that recovers travellers' trips after airline disruptions at scale (120,000+ trips per year): flight, hotel and dining agents cooperating, owned by different teams.

## Answer

Requirements: recover within minutes, respect policy and preferences, never double-book or leave partial states, ask travellers only when necessary, and be auditable.

Architecture:
- Event ingestion: airline disruption feeds onto a queue, then a trip-matching service, which creates one recovery run per affected trip (idempotent by trip and disruption id).
- Orchestrator agent (owned by the trip team): builds the recovery plan and coordinates the domain agents over A2A: a flight agent (airline team), a hotel agent (lodging team) and a dining agent (partner team). Each advertises an Agent Card with skills and auth requirements. Tasks are tracked through their states (submitted, working, input-required, completed, failed), with streaming or push notifications.
- Saga coordination: the orchestrator runs hold flight, then adjust the hotel, then move dining, then confirm, with compensations (release the hold, restore the hotel), idempotency keys per step, and a persisted saga log.
- Human-in-the-loop: the traveller's approval via app or push for options outside the pre-authorised rules. An `input-required` task state pauses the flow durably.
- Decision logic: deterministic ranking tools for options (constraints, policy, cost), and LLMs for interpreting preferences, explaining trade-offs and handling unusual cases.
- Reliability: per-agent timeouts and circuit breakers, fallbacks (rail options, a human travel desk), deadline propagation, fair scheduling during mass disruptions, and backpressure.
- Security: per-agent least-privilege credentials, signed Agent Cards, on-behalf-of traveller tokens, and an audit trail of every action.
- Observability: end-to-end traces across A2A hops, recovery time (for example from 45 minutes to 90 seconds), success and acceptance rates, cost deltas and escalations.

## Likely follow-ups

- What happens if the hotel agent succeeds but its response is lost before the orchestrator records it?
- How do you roll out a new version of the flight agent without breaking in-flight recoveries?

---

[← Q0499](../../batch_05_agentic_patterns_orchestration/0499_design_an_agentic_orchestration_platform_for_llm_suite/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md)
