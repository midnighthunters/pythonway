# Q0089 · Explaining LLM limitations to business stakeholders

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Communication | Easy |

## Question

A Finance director asks, "Can we trust the AI's answers?" How do you explain LLM limitations and controls in plain language?

## Answer

Keep it concrete and balanced:
- What it is: "It predicts likely text based on patterns and the documents we give it. It's very good at drafting, summarising and finding information, and it doesn't truly 'know' facts."
- Where it fails: it can state wrong things confidently, especially numbers, recent events, or questions our documents don't cover. It can be inconsistent between runs.
- How we control it: answers come from approved sources with citations, it says when it can't find an answer, numbers are checked by tools, sensitive actions need human approval, and we test it on real Finance examples before release and monitor it after.
- How to use it: as a fast first draft or research assistant that a person reviews, not as the final authority for filings or decisions.

Offer the evidence: the evaluation results on their own examples and the error rate, and agree a review process.

## Likely follow-ups

- How would you set expectations for accuracy numbers without over-promising?

---

[← Q0088](../../batch_01_llm_fundamentals/0088_handling_a_stream_that_breaks_mid_response/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0090 →](../../batch_01_llm_fundamentals/0090_model_documentation_for_model_risk_management/README.md)
