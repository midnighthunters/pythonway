# Q0889 · Kubernetes Deployment, Service, and ConfigMap for GenAI microservice

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Medium |

## Question

Write Kubernetes manifests (Deployment, Service, and ConfigMap) for deploying a scalable FastAPI GenAI microservice with resource limits, liveness probes, and security contexts.

## Answer

Enterprise cloud deployment requires Declarative Kubernetes manifests with explicit resource requests/limits to prevent noisy neighbor problems and ensure predictable scheduling.

```python
# no-run
# Kubernetes Production Deployment YAML
K8S_MANIFEST = '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-suite-service
  namespace: genai-platform
  labels:
    app: llm-suite-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-suite-service
  template:
    metadata:
      labels:
        app: llm-suite-service
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
      containers:
      - name: fastapi-app
        image: registry.jpmc.internal/genai/llm-suite:v2.4.1
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: "1000m"
            memory: "1Gi"
          limits:
            cpu: "2000m"
            memory: "2Gi"
        livenessProbe:
          httpGet:
            path: /livez
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: llm-suite-service
  namespace: genai-platform
spec:
  type: ClusterIP
  selector:
    app: llm-suite-service
  ports:
  - port: 80
    targetPort: 8000
'''
```

## Likely follow-ups

- Why should CPU limits be omitted or set carefully to avoid CPU throttling in multi-threaded runtimes?
- How does Kubernetes handle pod eviction when a container breaches its memory limit (`OOMKilled`)?

---

[← Q0888](../../batch_09_genai_services_fastapi/0888_uvicorn_loop_optimization_with_uvloop_and_httptools_in/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0890 →](../../batch_09_genai_services_fastapi/0890_horizontal_pod_autoscaler_using_custom_prometheus_metrics/README.md)
