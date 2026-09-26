# Q0387 · Evaluation run manifest

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Evaluation integrity | Easy |

## Question

Implement an immutable evaluation run manifest that captures everything needed to reproduce a run, with a stable fingerprint and JSON export.

## Answer

```python
import hashlib
import json
from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class RunManifest:
    dataset_sha: str
    code_commit: str
    model: str
    prompt_versions: dict[str, str]
    params: dict[str, float]
    judge: str
    index_version: str
    seed: int
    repeats: int = 3
    notes: str = field(default="", compare=False)

    def fingerprint(self) -> str:
        d = asdict(self)
        d.pop("notes")
        return hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()[:16]

    def to_json(self) -> str:
        return json.dumps({**asdict(self), "fingerprint": self.fingerprint()}, sort_keys=True, indent=2)


m1 = RunManifest("ds-9f2a", "c0ffee1", "model-x-2026-05-01", {"qa": "1.3.0"}, {"temperature": 0.0},
                 "judge-y-2026-03", "idx-42", seed=7, notes="baseline")
m2 = RunManifest("ds-9f2a", "c0ffee1", "model-x-2026-05-01", {"qa": "1.3.0"}, {"temperature": 0.0},
                 "judge-y-2026-03", "idx-42", seed=7, notes="rerun by Priya")
assert m1.fingerprint() == m2.fingerprint()
assert RunManifest(**{**asdict(m1), "model": "model-x-2026-09-01"}).fingerprint() != m1.fingerprint()
assert json.loads(m1.to_json())["fingerprint"] == m1.fingerprint()
```

Attach the manifest to every report and gate decision. Two runs with the same fingerprint should differ only by model non-determinism, and a different fingerprint tells you exactly what changed.

## Likely follow-ups

- Which of these fields would you require before a result can be used in a release decision?

---

[← Q0386](../../batch_04_llm_evaluation_observability/0386_reproducible_evaluations/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0388 →](../../batch_04_llm_evaluation_observability/0388_reporting_evaluation_results_to_stakeholders/README.md)
