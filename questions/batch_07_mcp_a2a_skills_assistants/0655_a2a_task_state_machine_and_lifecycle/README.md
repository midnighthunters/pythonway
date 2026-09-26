# Q0655 · A2A Task state machine and lifecycle

| Section | Topic | Difficulty |
|---|---|---|
| MCP, A2A, Agent Skills & Personal AI Assistants | A2A protocol | Medium |

## Question

Describe the complete A2A task lifecycle state machine. Write Python code implementing the state transition rules and detecting invalid state transitions.

## Answer

In the A2A protocol, a Task progresses through standard lifecycle states:
1. `submitted`: Task created by caller; queued for execution.
2. `working`: Agent actively running reasoning loops and tools.
3. `needs_input`: Agent paused waiting for additional data, clarification, or human approval.
4. `completed`: Task finished successfully with final output parts. (Terminal)
5. `failed`: Task encountered an unrecoverable error. (Terminal)
6. `cancelled`: Task terminated by caller before completion. (Terminal)

```python
from typing import Set


class A2ATaskStateMachine:
    VALID_STATES = {"submitted", "working", "needs_input", "completed", "failed", "cancelled"}
    TERMINAL_STATES = {"completed", "failed", "cancelled"}

    ALLOWED_TRANSITIONS = {
        "submitted": {"working", "cancelled", "failed"},
        "working": {"needs_input", "completed", "failed", "cancelled"},
        "needs_input": {"working", "cancelled", "failed"},
        "completed": set(),
        "failed": set(),
        "cancelled": set(),
    }

    def __init__(self, initial_state: str = "submitted"):
        if initial_state not in self.VALID_STATES:
            raise ValueError(f"Invalid initial state: {initial_state}")
        self.current_state = initial_state

    def transition(self, new_state: str) -> None:
        if new_state not in self.VALID_STATES:
            raise ValueError(f"Unknown state: {new_state}")
        if new_state not in self.ALLOWED_TRANSITIONS[self.current_state]:
            raise ValueError(f"Illegal state transition from '{self.current_state}' to '{new_state}'")
        self.current_state = new_state

    @property
    def is_terminal(self) -> bool:
        return self.current_state in self.TERMINAL_STATES


sm = A2ATaskStateMachine("submitted")
sm.transition("working")
sm.transition("needs_input")
sm.transition("working")
sm.transition("completed")
assert sm.is_terminal is True

try:
    sm.transition("working")
    assert False, "Should raise ValueError on transition from terminal state"
except ValueError as err:
    assert "Illegal state transition" in str(err)
```

## Likely follow-ups

- How does the calling agent resume a task in the `needs_input` state?
- What timeouts should be placed on tasks lingering in `submitted` or `working`?

---

[← Q0654](../../batch_07_mcp_a2a_skills_assistants/0654_validating_an_a2a_agent_card_against_json_schema/README.md) · [MCP, A2A, Agent Skills & Personal AI Assistants index](../README.md) · [All sections](../../README.md) · [Q0656 →](../../batch_07_mcp_a2a_skills_assistants/0656_a2a_task_creation_and_submission/README.md)
