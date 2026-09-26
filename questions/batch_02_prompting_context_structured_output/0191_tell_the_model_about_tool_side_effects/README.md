# Q0191 · Tell the model about tool side effects

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Tool use | Medium |

## Question

How should tool definitions and prompts communicate side effects (sending email, moving money), and what must be enforced outside the model?

## Answer

In the definitions:
- Say it plainly in the description: "Sends an email immediately to external recipients. Irreversible."
- Use annotations or metadata (MCP: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`), and have your own registry mark tools as read, write or financial.
- Separate "draft" and "commit" tools (`draft_email` and `send_email`, `prepare_transfer` and `execute_transfer`), so the model's default path is non-destructive.

In the prompt: "Before any write action, summarise what you'll do and ask the user to confirm."

Outside the model (non-negotiable):
- Human-in-the-loop approval for side-effecting calls (for example LangGraph `interrupt` or HITL middleware), with the exact arguments shown to the user.
- Authorisation per call against the user's entitlements and limits.
- Idempotency keys, so retries can't double-send or double-pay.
- Audit logging of who approved what, and rate limits.

## Likely follow-ups

- Why do "draft" and "commit" tool pairs improve safety even with approvals?

---

[← Q0190](../../batch_02_prompting_context_structured_output/0190_handoff_payload_between_agents/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0192 →](../../batch_02_prompting_context_structured_output/0192_design_outputs_for_evaluation/README.md)
