# Q0493 · SLOs for agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Operations | Medium |

## Question

What SLOs make sense for an agent service, which does multi-step work rather than single responses?

## Answer

- Availability: the fraction of runs that start and reach a terminal state without platform errors.
- Latency: time to first visible progress (for example a status event under 2 seconds), and time to completion per task type (p95 under N seconds for interactive tasks, or a deadline for background jobs).
- Task success: the fraction of runs completing successfully, as verified by final-state checks or downstream confirmation, per task type. Often an objective rather than a hard SLO, because it depends on inputs.
- Escalation rate within a target band (too high means the agent isn't useful, and zero may mean it's over-confident).
- Safety: zero unauthorised actions, and policy-violation rate below a threshold. These are treated as incidents rather than budgets.
- Cost per successful task within budget.

Measure per tenant and task type, with error budgets for availability and latency. Quality objectives drive release gates and reviews rather than paging.

## Likely follow-ups

- Why shouldn't task success rate page the on-call engineer?

---

[← Q0492](../../batch_05_agentic_patterns_orchestration/0492_multi_tenant_agent_platform_concerns/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0494 →](../../batch_05_agentic_patterns_orchestration/0494_fair_scheduling_of_agent_jobs_across_tenants/README.md)
