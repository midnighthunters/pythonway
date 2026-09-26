# B0051 · Solving a hard problem creatively

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Behavioral - problem solving | Medium |

## Question

Tell me about a time you solved a tough technical problem with a creative approach.

## Answer

The JD asks for "creative approaches to solve complex technical challenges".

- Situation: tool-selection accuracy collapsed as an agent's catalogue grew to 80 tools, and the context window was bloated.
- Action: reframed the problem. Instead of prompting harder, you added retrieval over tool descriptions (embed the tool docs, select the top-k tools per turn), grouped tools into bundles loaded on demand, and built a 300-query evaluation set to measure selection accuracy.
- Result: accuracy 71% → 93%, prompt tokens down 60%, latency down 35%.

Explain the insight (why the conventional approach failed) and how you validated the new one.

## Likely follow-ups

- Which alternatives did you reject?
- How did you convince others it was safe?

---

[← B0050](../../behavioural_questions/0050_working_with_different_working_styles/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0052 →](../../behavioural_questions/0052_iterating_quickly_on_feedback/README.md)
