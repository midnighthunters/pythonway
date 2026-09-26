# Q0403 · Anatomy of an agent loop

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent foundations | Easy |

## Question

Walk through the components of a production agent loop and what each is responsible for.

## Answer

1. Context assembly: system instructions, the task, relevant memory, tool definitions (only the allowed ones), and the conversation or scratchpad state.
2. Model call: the LLM decides on a tool call (or several) or a final answer. Use structured tool calling with validated arguments.
3. Policy checks: is this tool allowed for this user and task? Does it need approval? Is it within budget?
4. Execution: run the tool with timeouts, retries (for idempotent calls) and idempotency keys (for writes).
5. Observation handling: format and truncate the result, and mark untrusted content as data.
6. State update: append to history, update structured state, and checkpoint.
7. Stop check: final answer, step, token or cost limits, repeated-action detection, or a human interrupt.
8. Output: the final answer with evidence, plus an action log for audit.

Around it: tracing of every step, evaluation of trajectories, and error handling that returns useful errors to the model instead of crashing.

## Likely follow-ups

- Which of these components must never be delegated to the model?

---

[← Q0402](../../batch_05_agentic_patterns_orchestration/0402_workflows_versus_agents/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0404 →](../../batch_05_agentic_patterns_orchestration/0404_minimal_react_loop_with_a_fake_model/README.md)
