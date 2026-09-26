# Q0153 · Writing good tool descriptions

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Tool use | Medium |

## Question

Tool selection accuracy depends heavily on the tool definitions. What makes a good tool name, description and parameter schema?

## Answer

- Name: a verb and object, unambiguous, consistent across tools (`search_policies`, `get_account_balance`). Avoid near-duplicates the model can confuse.
- Description: what it does, when to use it and when not to ("Use for questions about internal HR policy. Not for payroll figures, use get_payslip"), what it returns, and any side effects or costs.
- Parameters: specific types, enums for fixed values, formats and examples in descriptions ("ISO date YYYY-MM-DD"), required versus optional, sensible defaults, and units ("amount in minor units").
- Outputs: concise, structured results with ids for follow-up calls, errors that explain how to fix the call, and pagination for large results.
- Granularity: prefer a few well-designed, task-level tools over dozens of thin API wrappers. Too many similar tools degrade selection.
- Safety: mark destructive or side-effecting tools (MCP has annotations such as `readOnlyHint` and `destructiveHint`) and require confirmation for them in code.

Evaluate tool selection with a test set of queries and expected tool calls, and iterate on the descriptions like any prompt.

## Likely follow-ups

- How would you detect that two tools are being confused by the model?

---

[← Q0152](../../batch_02_prompting_context_structured_output/0152_minimal_json_schema_validator/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0154 →](../../batch_02_prompting_context_structured_output/0154_select_relevant_tools_for_the_context/README.md)
