# Q0566 · Cron jobs for agents

| Section | Topic | Difficulty |
|---|---|---|
| LangGraph & LangChain in Practice | LangGraph Server | Easy |

## Question

How would you schedule recurring agent runs (a daily briefing, a nightly reconciliation check), and what should you watch out for?

## Answer

- Scheduling: LangGraph Platform cron jobs, or the platform scheduler (Kubernetes CronJobs, EventBridge Scheduler, Logic Apps) calling your run API with the assistant, input and thread strategy (a new thread per run, or a persistent thread per user).
- Identity: scheduled runs act on behalf of a user or a service identity, with explicitly scoped permissions. Re-check entitlements each run.
- Idempotency: one run per schedule slot (a dedupe key of job id plus date), so retries or overlapping schedulers don't double-send briefings.
- Load shaping: stagger start times (jitter) across many users to avoid provider rate-limit spikes, and put the runs in a lower-priority lane than interactive traffic.
- Observability: per-job success and failure metrics, alerts on consecutive failures, and user-visible history.
- Lifecycle: disable jobs for leavers, and give users an easy opt-out.

## Likely follow-ups

- How would you prevent 200,000 briefings from all starting at 07:00:00?

---

[← Q0565](../../batch_06_langgraph_langchain/0565_background_runs_and_webhooks/README.md) · [LangGraph & LangChain in Practice index](../README.md) · [All sections](../../README.md) · [Q0567 →](../../batch_06_langgraph_langchain/0567_streaming_agents_to_a_web_front_end/README.md)
