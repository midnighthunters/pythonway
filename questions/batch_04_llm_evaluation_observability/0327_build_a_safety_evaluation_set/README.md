# Q0327 · Build a safety evaluation set

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Safety evaluation | Medium |

## Question

What should a safety evaluation set for an internal banking assistant contain?

## Answer

- Policy-violating requests: harassment, discrimination, self-harm (with the expected supportive redirect), illegal activity (fraud, sanctions evasion, market abuse), and malware.
- Domain-specific risks: requests for personalised investment advice, insider or material non-public information, customer PII, and attempts to bypass controls ("how do I split payments to avoid reporting?").
- Jailbreaks and prompt injection: role-play, encodings, multi-turn escalation, and injected instructions in documents and tool outputs.
- Data leakage: attempts to extract the system prompt, other users' data, or restricted documents (paired with entitlement personas).
- Over-refusal probes: legitimate but sensitive-sounding requests (security training, compliance investigations, HR policy on misconduct), which must be answered.
- Multilingual and obfuscated variants.

For each case, record the expected behaviour (refuse, safe-complete, answer) and the severity. Run it on every model or prompt change, and track the attack success rate and over-refusal rate over time.

## Likely follow-ups

- How would you keep the jailbreak set current as new attack styles appear?

---

[← Q0326](../../batch_04_llm_evaluation_observability/0326_abstention_quality_metrics/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0328 →](../../batch_04_llm_evaluation_observability/0328_refusal_and_over_refusal_rates/README.md)
