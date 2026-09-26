# Q0895 · Ephemeral volume mounts and RAM disks for temporary file processing

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Easy |

## Question

Write Python code demonstrating the use of an in-memory `tempfile` / RAM disk for transient document processing, ensuring files are wiped immediately upon completion.

## Answer

When parsing customer bank statements or proprietary financial spreadsheets for RAG embeddings, saving files to standard persistent disks risks forensic data exposure if unencrypted. Processing inside RAM (`/dev/shm` or Python `io.BytesIO`) guarantees automatic destruction upon process completion.

```python
import tempfile
import os


def process_confidential_document(content_bytes: bytes) -> dict:
    # Process inside NamedTemporaryFile with automatic deletion
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        tmp.write(content_bytes)
        tmp.flush()
        file_path = tmp.name

        # Verify temporary file exists while context is active
        assert os.path.exists(file_path)
        processed_data = {"size": len(content_bytes), "status": "indexed"}

    # Once context exits, file is wiped from disk
    assert not os.path.exists(file_path)
    return processed_data


result = process_confidential_document(b"Confidential Mergers & Acquisitions Dossier")
assert result["status"] == "indexed"
assert result["size"] == 43
```

## Likely follow-ups

- How do you configure an `emptyDir` with `medium: Memory` in Kubernetes pod specs?
- What is the difference between `/tmp` and `/dev/shm` (shared memory) in Linux containers?

---

[← Q0894](../../batch_09_genai_services_fastapi/0894_managing_secrets_securely_with_vault_and_aws_secrets/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0896 →](../../batch_09_genai_services_fastapi/0896_container_security_scanning_and_minimal_base_images/README.md)
