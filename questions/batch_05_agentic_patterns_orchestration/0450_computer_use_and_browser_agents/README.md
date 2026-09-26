# Q0450 · Computer-use and browser agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Agent types | Medium |

## Question

What are computer-use (GUI) agents, and what extra risks and controls do they need compared with API-based agents?

## Answer

- They perceive the screen (screenshots, the accessibility tree or the DOM) and act with mouse, keyboard or browser automation. They are used where no API exists: legacy apps, web portals, internal tools.
- Loop: perceive, then decide, then act, then verify that the screen changed as expected.

Extra risks:
- Brittleness: UI changes, pop-ups and timing issues. Actions may land on the wrong element.
- Prompt injection from anything visible on screen (web pages, emails, documents).
- Broad privileges: the agent inherits the session's full access.
- Irreversible clicks (submit, pay, delete), and data exfiltration through form fields or URLs.

Controls: run in isolated VMs or browser profiles with minimal logged-in access, domain allowlists, a confirm step before submit, pay or delete actions, screenshots in the audit log, verification after each action, step limits, and a preference for APIs wherever they exist. Evaluate on recorded, versioned UI environments.

## Likely follow-ups

- Why should you prefer an API even when a computer-use agent can do the task?

---

[← Q0449](../../batch_05_agentic_patterns_orchestration/0449_sandboxed_code_execution_tool/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0451 →](../../batch_05_agentic_patterns_orchestration/0451_perceive_act_verify_loop/README.md)
