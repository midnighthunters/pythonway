# B0084 · Executive complains about a hallucination

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Stakeholder management | Medium |

## Question

A senior executive complains that LLM Suite gave them a confidently wrong answer in an important meeting. How do you respond?

## Answer

- Respond quickly and personally, acknowledge the impact and get specifics (prompt, time, conversation ID).
- Investigate with traces: model, retrieved sources, prompt version. Classify the cause: no grounding, a bad source, a model error or an ambiguous question.
- Explain in plain language what happened and what you are doing, without defensiveness or blaming "the model".
- Fix the specific case (correct the source, tune retrieval, add a guardrail), add it to the evaluation set, and consider UX changes such as prominent citations or prompts to verify.
- Follow up with the executive, and use the case (anonymised) in user education.

## Likely follow-ups

- How do you explain residual hallucination risk to executives?
- Which UX patterns reduce over-reliance?

---

[← B0083](../../behavioural_questions/0083_using_data_to_make_a_decision/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0085 →](../../behavioural_questions/0085_accountability_when_an_agent_takes_a_wrong_action/README.md)
