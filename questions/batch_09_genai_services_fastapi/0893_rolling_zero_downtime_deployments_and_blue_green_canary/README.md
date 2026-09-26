# Q0893 · Rolling zero-downtime deployments and blue green canary rollouts

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Medium |

## Question

Compare Kubernetes RollingUpdate, Blue/Green, and Canary deployment strategies for mission-critical GenAI services with model version migrations.

## Answer

| Deployment Strategy | Mechanism | Pros | Cons / Banking Consideration |
|---|---|---|---|
| **RollingUpdate** | Pods replaced incrementally (e.g. `maxSurge: 25%`, `maxUnavailable: 0`) | Zero downtime, no extra hardware cost | Both old and new versions run concurrently; requires backward-compatible database schemas |
| **Blue/Green** | Standalone parallel environment deployed and tested; router flips 100% traffic instantaneously | Instant rollback if regression detected | Doubles infrastructure costs during deployment window |
| **Canary (Istio / Argo Rollouts)**| Routes small percentage (e.g. 5%) of live traffic to canary; evaluates error rate before promoting | Validates model accuracy and latency on real traffic with minimal blast radius | Requires automated metric analysis (Kayenta / Argo Rollouts Analysis) |

```python
# no-run
# Argo Rollouts Canary Strategy Manifest
CANARY_MANIFEST = '''
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: llm-suite-rollout
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 5
      - pause: { duration: 10m }
      - setWeight: 20
      - pause: { duration: 30m }
      - setWeight: 50
      - pause: { duration: 15m }
'''
```

## Likely follow-ups

- How do sticky sessions impact Canary routing in multi-turn chat applications?
- What automated health checks trigger automated canary abort and rollback?

---

[← Q0892](../../batch_09_genai_services_fastapi/0892_graceful_termination_lifecycle_in_kubernetes_prestop_hook/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0894 →](../../batch_09_genai_services_fastapi/0894_managing_secrets_securely_with_vault_and_aws_secrets/README.md)
