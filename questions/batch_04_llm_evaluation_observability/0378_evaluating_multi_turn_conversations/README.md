# Q0378 · Evaluating multi-turn conversations

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Conversation evaluation | Medium |

## Question

Single-turn evaluation misses many assistant failures. How do you evaluate multi-turn conversations?

## Answer

Failure modes that only show up in multi-turn: forgetting earlier constraints, drift from system rules over long sessions, bad handling of corrections ("no, I meant Paris"), clarifying questions asked too often or not at all, repeated tool calls, and gradual jailbreaks.

Methods:
- Scripted conversations: fixed multi-turn transcripts with expected behaviour at specific turns (the assistant must use the correction from turn 3).
- User simulators: an LLM plays a user with a persona and goal and interacts with the assistant until the goal is met or a turn limit is reached. Score task success, turns taken, and rule violations.
- Conversation-level judges: rubrics for coherence, consistency, efficiency and tone across the whole transcript.
- Replay of real sessions (with approval) where later turns are regenerated, to test changes in context.

Report task success, average turns to success, and per-turn violation rates, and run long-session variants (30+ turns) to test context management.

## Likely follow-ups

- How do you keep a user simulator from being too cooperative?

---

[← Q0377](../../batch_04_llm_evaluation_observability/0377_stratified_sampling_for_evaluation_sets/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0379 →](../../batch_04_llm_evaluation_observability/0379_user_simulator_for_conversation_evaluation/README.md)
