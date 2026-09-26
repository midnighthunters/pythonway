# Q0596 · Evaluate a LangGraph agent

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Evaluation | Medium |

## Question

How would you set up evaluation for a LangGraph agent before and after release?

## Answer

- Datasets: scenario cases with inputs, expected final outcomes, expected or forbidden trajectories (tools and nodes), and final-state checks against simulated backends. Include unanswerable, adversarial and approval cases.
- Offline runs: run the compiled graph over the dataset with a fixed agent version (graph, prompts, model), several repeats for pass^k, and fakes for irreversible tools. Collect the trajectories from stream updates or traces.
- Evaluators: final-answer correctness (rubric judges or exact checks), trajectory match (milestones in order, forbidden tools absent), tool-argument accuracy, final-state predicates, safety checks, and cost and latency per run. LangSmith experiments or your own harness can run these and compare versions side by side.
- CI gate: thresholds and "no critical regressions", run on every prompt, graph, tool or model change.
- Online: sample production traces for judge scoring, capture user feedback and escalations, monitor guard trips and loops, and feed failures back into the dataset.
- Human review: periodic expert review of sampled trajectories, especially the approval decisions and edge cases.

## Likely follow-ups

- How do you evaluate an agent whose valid trajectories vary?

---

[← Q0595](../../batch_06_langgraph_langchain/0595_human_in_the_loop_ux_with_langgraph/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0597 →](../../batch_06_langgraph_langchain/0597_design_a_langgraph_trade_break_agent/README.md)
