# Q0863 · Multipart form data with file parsing and simultaneous JSON metadata

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Medium |

## Question

Write Python code implementing a FastAPI endpoint accepting multipart form data that combines a file upload with structured JSON metadata parameters.

## Answer

In enterprise document processing, users frequently upload an invoice or pitchbook while supplying structured metadata (cost center, target extraction schema, classification tags) in the same HTTP request.

```python
import json
from io import BytesIO
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/process-document")
async def process_document(
    metadata: str = Form(...),  # Serialized JSON string
    file: UploadFile = File(...),
):
    meta_dict = json.loads(metadata)
    file_bytes = await file.read()
    return {
        "filename": file.filename,
        "department": meta_dict.get("department"),
        "doc_type": meta_dict.get("doc_type"),
        "size_bytes": len(file_bytes),
    }


client = TestClient(app)
meta_payload = json.dumps({"department": "Global Equities", "doc_type": "TermSheet"})

res = client.post(
    "/process-document",
    data={"metadata": meta_payload},
    files={"file": ("termsheet.pdf", BytesIO(b"%PDF-1.4 dummy"), "application/pdf")},
)

assert res.status_code == 200
assert res.json()["department"] == "Global Equities"
assert res.json()["filename"] == "termsheet.pdf"
```

## Likely follow-ups

- How does Pydantic model validation work with Form fields in FastAPI?
- What are the security risks of uploading un-sanitized PDF filenames?

---

[← Q0862](../../batch_09_genai_services_fastapi/0862_custom_pydantic_v2_validators_for_prompt_injection_patterns/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0864 →](../../batch_09_genai_services_fastapi/0864_content_negotiation_supporting_both_json_completion_and_sse/README.md)
