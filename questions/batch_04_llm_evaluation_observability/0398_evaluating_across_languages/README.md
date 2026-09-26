# Q0398 · Evaluating across languages

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation coverage | Medium |

## Question

The assistant will launch in English, French, German, Hindi and Japanese. How do you evaluate it without five times the effort?

## Answer

- Core set translation: professionally translate (or LLM-translate with human review) a representative core of the golden set. Keep culturally or locally specific cases native, written by local SMEs.
- Local content: add cases for local policies and terminology that only exist in that language or jurisdiction.
- Metrics per language: answer quality, retrieval hit rate (cross-lingual retrieval is often the weak point), faithfulness, refusal and safety behaviour, formatting (dates, numbers), and reply-language correctness.
- Judges: validate the judge's agreement with native-speaker labels per language. Judges can be weaker outside English.
- Prioritise by user volume and risk: full depth for the major languages, lighter checks for the rest, and expand as usage grows.
- Monitor per-language online signals (feedback, rephrasing) after launch.

## Likely follow-ups

- Why might an LLM judge be less reliable in Japanese than in English?

---

[← Q0397](../../batch_04_llm_evaluation_observability/0397_evaluating_an_mcp_tool_server/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0399 →](../../batch_04_llm_evaluation_observability/0399_design_an_evaluation_platform_for_llm_suite/README.md)
