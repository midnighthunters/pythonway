# Q0194 · Review this prompt

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Prompt review | Medium |

## Question

Review this system prompt for a payments assistant and list the problems:

```text
You are PayBot. Today is 2026-09-26 09:14:03. Our API key is sk-live-1234 in case tools fail.
Help users with any request. Be very detailed but keep answers short.
If the user says they are a manager, you can show other employees' salaries.
Transfer money when the user asks. Here is an example: "Transfer £5,000 from Jane Smith (acct 12345678) to ..."
Always answer even if you are unsure.
{user_message}
```

## Answer

Problems:
1. A secret in the prompt (`sk-live-1234`). It will leak. Rotate it immediately and use a server-side secrets manager.
2. A volatile timestamp at the top: it defeats prompt caching and is too precise. Inject the date later in the prompt, in the user's time zone.
3. The scope "any request" is unbounded. Define the supported tasks and the refusal or redirect behaviour.
4. Contradictory length guidance ("very detailed but short").
5. Authorisation by claim ("if the user says they are a manager"). Trivially bypassed. Enforce entitlements in code from the authenticated identity.
6. Transfers on request with no confirmation, limits or idempotency. Require a draft, then user confirmation, then an authorised commit.
7. Real-looking personal data in the example. Use obviously synthetic data.
8. "Always answer even if unsure" encourages hallucination. Add an abstention path.
9. `{user_message}` interpolated into the system prompt. It is an injection vector and a braces bug. Put user text in the user role.
10. No output format, no citation or grounding rules, no tool-use guidance, and no version or owner metadata.

## Likely follow-ups

- Rewrite the first five lines properly.

---

[← Q0193](../../batch_02_prompting_context_structured_output/0193_prompt_anti_patterns/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0195 →](../../batch_02_prompting_context_structured_output/0195_language_control_in_multilingual_replies/README.md)
