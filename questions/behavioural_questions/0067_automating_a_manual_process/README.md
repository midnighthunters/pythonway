# B0067 · Automating a manual process

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Behavioral - efficiency | Easy |

## Question

Tell me about a time you automated a manual process.

## Answer

- Situation: weekly prompt evaluation runs took four hours by hand and got skipped under pressure.
- Action: built a CI job that runs the evaluation suite on every prompt or model change, posts a diff report on the pull request and blocks merges on threshold regressions.
- Result: about 200 hours a year saved, three regressions caught before release, and evidence for audit.

## Likely follow-ups

- How did you make sure the automation was trustworthy?
- What did you choose not to automate?

---

[← B0066](../../behavioural_questions/0066_a_mistake_you_made_in_production/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0068 →](../../behavioural_questions/0068_working_under_pressure/README.md)
