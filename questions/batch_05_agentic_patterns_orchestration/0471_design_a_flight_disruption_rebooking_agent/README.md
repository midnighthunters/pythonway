# Q0471 · Design a flight-disruption rebooking agent

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent design | Hard |

## Question

Design an agent that, when a traveller's flight is cancelled, rebooks the flight and updates the hotel and dinner reservations, within minutes and safely.

## Answer

Trigger: an airline disruption event arrives on a queue, and the agent identifies the affected trips (booking lookup).

Flow (a graph with agentic nodes):
1. Assess: get the trip itinerary, traveller preferences and policy (cabin, budget, loyalty), and the constraints (must arrive before the meeting).
2. Search and rank alternatives (flights, alternate airports or rail) with deterministic constraint filtering and scoring. The LLM is used for explanation and edge-case judgement, not for arithmetic.
3. Propose to the traveller: the top options with trade-offs, via their channel, with one-tap approval. Auto-book only within pre-authorised rules (same cabin, below the price delta, arrives before the deadline).
4. Execute as a saga: hold the seat, then ticket, then update the hotel (shift the dates or cancel and rebook), then move the dinner. Each step is idempotent, with compensations (release the hold, restore the hotel) on failure.
5. Notify with the new itinerary, and update the expense and policy records.

Engineering: durable state per disruption (checkpointed), deadlines (seat availability disappears fast), parallel searches, circuit breakers on supplier APIs, human escalation when the fare rules block changes or it is repeatedly failing, and full audit.

Metrics: time to recovery (for example from 45 minutes to 90 seconds), rebooking success rate, traveller acceptance rate, cost delta against policy, and escalations.

## Likely follow-ups

- Which steps must never be automated without the traveller's explicit approval?

---

[← Q0470](../../batch_05_agentic_patterns_orchestration/0470_orchestrating_a_personal_ai_assistant/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0472 →](../../batch_05_agentic_patterns_orchestration/0472_rank_rebooking_options_under_constraints/README.md)
