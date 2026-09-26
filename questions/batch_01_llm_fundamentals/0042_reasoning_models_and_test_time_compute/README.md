# Q0042 · Reasoning models and test-time compute

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Model capabilities | Medium |

## Question

What are "reasoning" models, and how does using one change your application design, cost and latency?

## Answer

- Reasoning models are trained, largely with reinforcement learning on verifiable tasks, to produce an internal chain of thought before the final answer. More thinking tokens (test-time compute) generally means better accuracy on maths, coding, planning and multi-step analysis.
- APIs expose controls such as a reasoning effort or a thinking-token budget. The reasoning tokens are usually billed as output tokens, and are often hidden or only summarised.

Design implications:
- Latency and cost: TTFT can be seconds or more, so stream status updates and set timeouts appropriately.
- Routing: use them for hard steps (planning, complex extraction, code fixes) and a fast model for simple ones. A router or cascade pays off here.
- Prompting: give clear goals and constraints rather than step-by-step "think carefully" scripts. Few-shot examples help less, and sampling parameters may be fixed.
- Agents: fewer but smarter steps, which is good for tool-heavy workflows. Preserve reasoning state across tool calls where the API supports it.
- Evaluation: measure accuracy per unit of cost and latency. Higher effort isn't always worth it.

## Likely follow-ups

- How would you decide per request whether to use a reasoning model?
- Why shouldn't you log or display raw reasoning traces to end users without review?

---

[← Q0041](../../batch_01_llm_fundamentals/0041_mixture_of_experts_routing/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0043 →](../../batch_01_llm_fundamentals/0043_estimate_training_compute_with_6nd/README.md)
