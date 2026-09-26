# Q0891 · KEDA scaled object based on Redis queue depth

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Medium |

## Question

Write a KEDA (Kubernetes Event-driven Autoscaling) `ScaledObject` configuration to autoscale background Celery/ARQ worker pods from 0 to 50 based on Redis list queue length.

## Answer

When background document ingestion workloads are intermittent, keeping dozens of worker pods running 24/7 wastes cloud budget. KEDA allows scaling worker pods to zero when the Redis queue is empty, and automatically spinning up pods as new indexing tasks arrive.

```python
# no-run
# KEDA ScaledObject for Redis Queue
KEDA_SCALED_OBJECT = '''
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: celery-worker-scaler
  namespace: genai-platform
spec:
  scaleTargetRef:
    kind: Deployment
    name: celery-indexing-worker
  minReplicaCount: 0
  maxReplicaCount: 50
  cooldownPeriod: 300
  pollingInterval: 15
  triggers:
  - type: redis
    metadata:
      address: redis-master.genai-platform.svc.cluster.local:6379
      listName: queue_batch
      listLength: "10"
      enableTLS: "true"
    authenticationRef:
      name: keda-redis-auth
'''
```

## Likely follow-ups

- What is cold-start latency when scaling worker pods up from zero replicas?
- How does KEDA authenticate to Azure Service Bus or AWS SQS using Pod Identity / IRSA?

---

[← Q0890](../../batch_09_genai_services_fastapi/0890_horizontal_pod_autoscaler_using_custom_prometheus_metrics/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0892 →](../../batch_09_genai_services_fastapi/0892_graceful_termination_lifecycle_in_kubernetes_prestop_hook/README.md)
