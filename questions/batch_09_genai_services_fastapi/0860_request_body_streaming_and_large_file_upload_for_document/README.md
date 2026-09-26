# Q0860 · Request body streaming and large file upload for document RAG endpoints

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Medium |

## Question

Write Python code using FastAPI's `UploadFile` and chunked streaming to process large PDF/text files for RAG pipelines without reading the entire file into memory at once.

## Answer

Reading an entire 100MB financial filing into RAM using `file.read()` risks memory exhaustion when hundreds of concurrent analysts upload documents. Streaming chunks into a temporary file or downstream chunker maintains a constant memory footprint.

```python
from io import BytesIO
from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    total_bytes = 0
    chunk_count = 0
    # Stream in 16KB chunks
    while True:
        chunk = await file.read(16 * 1024)
        if not chunk:
            break
        total_bytes += len(chunk)
        chunk_count += 1

    return {
        "filename": file.filename,
        "total_bytes": total_bytes,
        "chunks_processed": chunk_count,
    }


client = TestClient(app)
dummy_file_content = b"JPMorgan Chase Annual Report Content. " * 1000

response = client.post(
    "/upload-document",
    files={"file": ("report.txt", BytesIO(dummy_file_content), "text/plain")},
)

assert response.status_code == 200
assert response.json()["total_bytes"] == len(dummy_file_content)
assert response.json()["chunks_processed"] >= 1
```

## Likely follow-ups

- How does `UploadFile` use `SpooledTemporaryFile` to spill from memory to disk above a size threshold?
- What file validation (magic byte checks, MIME type) must occur before parsing PDFs?

---

[← Q0859](../../batch_09_genai_services_fastapi/0859_health_checks_deep_versus_shallow_liveness_and_readiness/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0861 →](../../batch_09_genai_services_fastapi/0861_file_streaming_and_download_for_generated_pdf_and_excel/README.md)
