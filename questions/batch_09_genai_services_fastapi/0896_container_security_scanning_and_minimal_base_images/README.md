# Q0896 · Container security scanning and minimal base images

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Medium |

## Question

Explain container vulnerability scanning (Trivy, Grype, Prisma Cloud) and how minimal base images (Chainguard, distroless) mitigate Common Vulnerabilities and Exposures (CVEs).

## Answer

Standard base images like `python:3.11` (based on Debian) include hundreds of operating system utilities: `curl`, `bash`, `tar`, `apt`, `coreutils`. If any of these packages have an unpatched CVE, security scanners block enterprise deployment.

- **Minimal Distroless / Chainguard**: Contain *only* the Python runtime and minimal C-libraries (`glibc`/`musl`). No shell (`bash`), no package manager (`apt`), and no standard Unix utilities.
- **Benefits**:
  1. Image size drops from 1 GB to < 100 MB.
  2. Attackers cannot spawn interactive reverse shells (`/bin/sh` does not exist).
  3. Zero known CVEs reported during CI/CD security gating.

```python
# no-run
# Chainguard Python base image example
CHAINGUARD_DOCKERFILE = '''
FROM cgr.dev/chainguard/python:latest

WORKDIR /app

COPY --chown=nonroot:nonroot requirements.txt .
RUN pip install -r requirements.txt --user

COPY --chown=nonroot:nonroot . .

ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
```

## Likely follow-ups

- How do developers debug a running distroless container if it contains no shell? (Use `kubectl debug` with ephemeral debug containers).
- What is Software Bill of Materials (SBOM) generation (e.g. Syft)?

---

[← Q0895](../../batch_09_genai_services_fastapi/0895_ephemeral_volume_mounts_and_ram_disks_for_temporary_file/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0897 →](../../batch_09_genai_services_fastapi/0897_optimizing_container_startup_time_for_serverless_containers/README.md)
