# Q0593 · Debugging a stuck or looping graph

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | Debugging | Medium |

## Question

A production thread never finishes, or keeps looping. How do you debug it?

## Answer

1. Status: `get_state(thread)`. Look at `next` (which node is pending) and `tasks` (is there an unanswered interrupt?). Many "stuck" runs are simply waiting for a resume nobody sent, which means the notification path is broken.
2. History: `get_state_history(thread)`. Look at the sequence of nodes and updates. A repeating pattern means a loop: check the conditional edge's inputs at each step (a flag never set, a counter not incremented because of a reducer bug).
3. Trace: inspect the LLM inputs and outputs at the repeating step. The model may keep calling the same tool because the tool result format confuses it, or the error message gives no useful hint.
4. Reproduce: replay from a checkpoint locally with fake or recorded responses. Fork with `update_state` to test a fix (for example set the missing flag).
5. Fix and guard: correct the routing logic, add `RemainingSteps` or counter-based exits, add repetition detection, and add a trajectory test for the case.
6. Remediate the live thread: update its state or resume it, or cancel it and notify the user, and check for side effects already executed.

## Likely follow-ups

- How do you tell a thread waiting on an interrupt from one blocked on a hung tool call?

---

[← Q0592](../../batch_06_langgraph_langchain/0592_securing_a_langgraph_deployment/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0594 →](../../batch_06_langgraph_langchain/0594_side_effects_and_replays_in_langgraph/README.md)
