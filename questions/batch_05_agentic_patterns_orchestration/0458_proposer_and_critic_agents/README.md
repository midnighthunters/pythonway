# Q0458 · Proposer and critic agents

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Multi-agent | Medium |

## Question

Implement a proposer-critic loop in which the critic checks the proposal against tool evidence (not just opinion) and the proposer revises until the critic finds no issues, with a round cap.

## Answer

```python
import re
from typing import Callable


def propose_and_critique(task: str, propose: Callable[[str, list[str]], str], evidence: dict[str, str],
                         max_rounds: int = 3) -> dict:
    issues: list[str] = []
    history = []
    for rnd in range(1, max_rounds + 1):
        proposal = propose(task, issues)
        issues = [f"{k} should be {v}" for k, v in evidence.items()
                  if (m := re.search(rf"{k}\s*[:=]\s*([\w.]+)", proposal)) and m.group(1) != v]
        history.append({"round": rnd, "proposal": proposal, "issues": issues})
        if not issues:
            return {"accepted": proposal, "rounds": rnd, "history": history}
    return {"accepted": None, "rounds": max_rounds, "history": history}


def proposer(task: str, issues: list[str]) -> str:
    fx = "1.30"
    for issue in issues:
        if issue.startswith("fx"):
            fx = issue.split()[-1]
    return f"Convert 100 GBP: fx={fx}, total={float(fx) * 100:.2f} USD"


out = propose_and_critique("convert", proposer, {"fx": "1.2710"})
assert out["rounds"] == 2 and out["accepted"].startswith("Convert 100 GBP: fx=1.2710, total=127.10")
```

A critic grounded in evidence (tool results, tests, source documents) catches real errors. An ungrounded critic mostly generates stylistic churn. Use a different model or prompt for the critic, keep the round count small, and log disagreements for evaluation.

## Likely follow-ups

- When does adding a critic reduce accuracy?

---

[← Q0457](../../batch_05_agentic_patterns_orchestration/0457_escalate_to_a_human_with_context/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0459 →](../../batch_05_agentic_patterns_orchestration/0459_verify_agent_outputs_before_returning/README.md)
