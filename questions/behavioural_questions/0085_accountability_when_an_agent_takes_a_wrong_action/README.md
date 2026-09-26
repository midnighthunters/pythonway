# B0085 · Accountability when an agent takes a wrong action

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Responsible AI | Hard |

## Question

If an AI agent takes a wrong action, such as sending an incorrect email or updating the wrong record, who is accountable, and how should the system be designed?

## Answer

Accountability stays with people and the firm: the business owner of the process, the approving user where human-in-the-loop applies, and the engineering owners for design flaws. Under UK SM&CR-style regimes, named senior managers remain accountable for their areas; an agent does not change that.

Design implications:

- Classify actions (read, reversible write, irreversible) and gate high-impact ones behind approval.
- Use least-privilege, user-delegated credentials and record the agent's identity.
- Make actions idempotent, and provide undo or compensation plus a dry-run preview where possible.
- Keep a full audit trail: inputs, a reasoning summary, tool calls, approver.
- Monitor, keep a kill switch, and route failures into the incident process.

## Likely follow-ups

- Which actions should always need human approval?
- How would you implement undo for agent actions?

---

[← B0084](../../behavioural_questions/0084_executive_complains_about_a_hallucination/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0086 →](../../behavioural_questions/0086_your_first_90_days_on_the_team/README.md)
