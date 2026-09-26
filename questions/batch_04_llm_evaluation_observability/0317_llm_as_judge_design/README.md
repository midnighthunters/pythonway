# Q0317 · LLM-as-judge design

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Model-graded evaluation | Medium |

## Question

How do you design a reliable LLM-as-judge evaluator?

## Answer

- Narrow, well-defined criteria: one judge per dimension (faithfulness, relevance, completeness, tone) rather than one vague "quality" score.
- A rubric with concrete anchors for each score ("1 = contradicts the sources, 3 = partially supported, 5 = every claim supported"), with examples.
- Give the judge what it needs: the question, the answer, the retrieved sources and the reference answer if one exists. Judges verify far better than they solve from scratch.
- Structured output: scores plus a short rationale and evidence, in a strict schema. Binary or 3-point scales are often more reliable than 10-point ones.
- Bias controls: randomise or swap positions in pairwise comparisons, control for length, and use a different model family from the one being judged where possible.
- Calibrate against human labels (agreement or kappa) before trusting it, and re-calibrate when the judge model or rubric changes.
- Low temperature, pinned judge version, cost budget, and sampling for online use.

## Likely follow-ups

- How would you evaluate the judge itself?

---

[← Q0316](../../batch_04_llm_evaluation_observability/0316_pass_k_reliability_for_agents/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0318 →](../../batch_04_llm_evaluation_observability/0318_judge_prompt_with_rubric_and_structured_verdict/README.md)
