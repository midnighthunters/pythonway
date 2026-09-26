# Q0751 · Azure OpenAI Assistants API with Code Interpreter in banking

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | Azure OpenAI | Medium |

## Question

How is the Azure OpenAI Assistants API with Code Interpreter deployed in an enterprise bank, and what security controls sandbox the Python execution environment?

## Answer

The Azure OpenAI Assistants API provides persistent threads, managed file search, and an integrated sandboxed Python runtime (Code Interpreter) for data analysis and math.

Enterprise Banking Architecture & Security Controls:
1. Sandboxed Python Runtime:
   - The Code Interpreter executes inside an isolated, short-lived virtualized container managed by Microsoft within the Azure tenant boundary.
   - Network access from inside the Code Interpreter is completely disabled (`--network none`), preventing exfiltration of ingested banking data.
2. File Ephemerality & Data Isolation:
   - Financial datasets (e.g. CSV trade logs) uploaded to a thread are encrypted at rest with customer-managed keys (CMEK) and accessible only to that thread.
   - Files are automatically deleted when the thread or assistant is deleted.
3. Use Cases:
   - Quantitative finance: running Monte Carlo simulations, plotting yield curves, and recalculating amortization schedules on uploaded spreadsheets without deploying custom Python worker pods.

## Likely follow-ups

- Why cannot Code Interpreter connect directly to an internal corporate SQL database?
- How does the Assistants API manage token context when code outputs large stdout text?

---

[← Q0750](../../batch_08_azure_openai_bedrock_cloud_ai/0750_building_an_opentelemetry_span_formatter_for_llm_invocations/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0752 →](../../batch_08_azure_openai_bedrock_cloud_ai/0752_asynchronous_file_batch_analysis_pipeline_with_azure_openai/README.md)
