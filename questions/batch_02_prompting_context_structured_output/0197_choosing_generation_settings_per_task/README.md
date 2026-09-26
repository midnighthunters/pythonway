# Q0197 · Choosing generation settings per task

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Generation settings | Easy |

## Question

What temperature, output limit and format settings would you use for extraction, classification, summarisation, drafting and agent tool calls?

## Answer

- Extraction and classification: temperature about 0, strict structured output, a modest `max_tokens`, and logprobs if available for confidence.
- Tool-calling agents: low temperature (0–0.3), tool choice set to auto (or forced for single-step tasks), parallel tool calls enabled only where the tools are safe to run concurrently.
- Summarisation of source documents: low temperature (0–0.3), a length specified in structure, a faithfulness instruction, and `max_tokens` with headroom.
- Drafting (emails, reports): moderate temperature (0.5–0.8) for natural wording, style guide in the prompt, lint afterwards.
- Brainstorming: higher temperature, or several samples.
- Reasoning models: set the effort level instead of temperature. Many ignore or fix sampling parameters.

Store the settings with the prompt version (they're part of the behaviour contract), and evaluate them together.

## Likely follow-ups

- Why should sampling settings be versioned together with the prompt?

---

[← Q0196](../../batch_02_prompting_context_structured_output/0196_few_shot_examples_from_production_data/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0198 →](../../batch_02_prompting_context_structured_output/0198_prompt_debugging_workflow/README.md)
