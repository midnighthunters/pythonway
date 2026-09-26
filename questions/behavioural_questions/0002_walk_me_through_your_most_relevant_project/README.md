# B0002 · Walk me through your most relevant project

| Section | Topic | Difficulty |
|---|---|---|
| Behavioural, Role & JPMorganChase | Introduction | Medium |

## Question

Walk me through the project on your CV that is most relevant to this role, end to end.

## Answer

Give a system tour the interviewer can probe at any point:

- Problem and users: who used it, what pain it removed, the success metric.
- Architecture: request path (client → FastAPI → orchestration/agent → model provider → tools/data), where state lives, how it is deployed (containers on AKS/EKS/ECS, serverless).
- Your role: decisions you owned, alternatives you rejected and why.
- Hard parts: one technical (streaming through a gateway, tool-call reliability) and one organisational (security review, data-access approvals).
- Operations: monitoring, SLOs, incidents, cost.
- Results: adoption, latency, accuracy, cost per request.
- Retrospective: what you would change at 10x scale.

Have a diagram you can draw in two minutes. JPMorganChase interviewers often ask candidates to design their own past system and then scale or critique it.

## Likely follow-ups

- What breaks first at 10x traffic?
- What would you do differently today?
- How did you test and evaluate it?

---

[← B0001](../../behavioural_questions/0001_tell_me_about_yourself/README.md) · [Behavioural, Role & JPMorganChase index](../README.md) · [All sections](../../README.md) · [B0003 →](../../behavioural_questions/0003_why_jpmorganchase/README.md)
