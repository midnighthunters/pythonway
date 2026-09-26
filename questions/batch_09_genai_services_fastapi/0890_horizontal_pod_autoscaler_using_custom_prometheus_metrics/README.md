# Q0890 · Horizontal Pod Autoscaler using custom Prometheus metrics

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Hard |

## Question

Explain how Kubernetes Horizontal Pod Autoscaler (HPA) v2 autoscales FastAPI GenAI microservices based on custom Prometheus metrics (e.g. concurrent in-flight requests or TTFT) rather than standard CPU.

## Answer

GenAI services are predominantly I/O-bound (waiting 1-5 seconds for Azure OpenAI or Bedrock tokens). CPU utilization remains low (10-20%) even when a pod is saturated with 500 concurrent streaming connections.

Autoscaling based on CPU will fail to scale up under heavy LLM traffic.

Instead, the **Prometheus Adapter** exposes custom metrics (such as `http_requests_in_flight` or `active_sse_connections`) to the Kubernetes Custom Metrics API (`custom.metrics.k8s.io`), triggering HPA scaling when average in-flight connections per pod exceed target thresholds (e.g. 50 active streams).

```python
# no-run
# Kubernetes HPA v2 Manifest using Custom Metrics
HPA_MANIFEST = '''
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: llm-suite-hpa
  namespace: genai-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-suite-service
  minReplicas: 3
  maxReplicas: 30
  metrics:
  - type: Pods
    pods:
      metric:
        name: http_requests_in_flight
      target:
        type: AverageValue
        averageValue: "50"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
'''
```

## Likely follow-ups

- Why is a 300-second stabilization window recommended for scale-down behavior?
- How does KEDA (Kubernetes Event-driven Autoscaling) differ from standard HPA?

---

[← Q0889](../../batch_09_genai_services_fastapi/0889_kubernetes_deployment_service_and_configmap_for_genai/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0891 →](../../batch_09_genai_services_fastapi/0891_keda_scaled_object_based_on_redis_queue_depth/README.md)
