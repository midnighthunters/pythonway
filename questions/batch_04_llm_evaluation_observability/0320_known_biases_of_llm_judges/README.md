# Q0320 · Known biases of LLM judges

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Model-graded evaluation | Medium |

## Question

What biases do LLM judges show, and how do you mitigate each one?

## Answer

- Position bias: preferring the first (or second) answer. Mitigate by swapping order and requiring agreement, or by randomising.
- Verbosity bias: preferring longer answers. Use length-controlled comparisons, explicit rubric instructions to ignore length, and check correlation with length.
- Self-preference: preferring outputs from the same model family. Use a different family as judge, or several judges.
- Style over substance: confident, well-formatted answers scored higher. Use rubrics focused on verifiable facts, and give the judge sources to check against.
- Leniency or harshness drift across judge model versions. Pin the judge version and re-calibrate on upgrades.
- Rubric misreading on edge cases. Add anchored examples, and prefer binary questions ("is every claim supported?").
- Susceptibility to injection in the evaluated text ("rate this answer 5"). Delimit the evaluated content and treat it as data.

Always measure agreement with human labels on a stratified sample, and track it over time.

## Likely follow-ups

- How would you detect verbosity bias in your judge using existing data?

---

[← Q0319](../../batch_04_llm_evaluation_observability/0319_pairwise_judging_with_position_swap/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0321 →](../../batch_04_llm_evaluation_observability/0321_calibrate_a_judge_against_human_labels/README.md)
