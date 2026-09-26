# Q0861 · File streaming and download for generated PDF and Excel reports

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | FastAPI foundations | Easy |

## Question

Write Python code using FastAPI's `StreamingResponse` to stream a generated binary file (CSV/Excel report) to the client with appropriate `Content-Disposition` headers.

## Answer

When an agent completes a financial research workflow, returning a CSV or Excel attachment requires streaming bytes with headers that prompt the user's browser to download the file.

```python
from io import StringIO
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient

app = FastAPI()


def generate_portfolio_csv():
    '''Generator yielding CSV rows.'''
    yield "Ticker,Shares,Price,MarketValue\n"
    yield "AAPL,100,225.50,22550.00\n"
    yield "MSFT,200,440.00,88000.00\n"
    yield "JPM,150,210.00,31500.00\n"


@app.get("/export/portfolio")
def export_portfolio():
    return StreamingResponse(
        generate_portfolio_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=portfolio_report.csv"},
    )


client = TestClient(app)
res = client.get("/export/portfolio")

assert res.status_code == 200
assert res.headers["content-type"].startswith("text/csv")
assert "attachment; filename=portfolio_report.csv" in res.headers["content-disposition"]
assert "JPM,150,210.00,31500.00" in res.text
```

## Likely follow-ups

- Why is streaming preferable to writing the file to disk and serving via `FileResponse`?
- How do you clean up temporary files generated during PDF rendering?

---

[← Q0860](../../batch_09_genai_services_fastapi/0860_request_body_streaming_and_large_file_upload_for_document/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0862 →](../../batch_09_genai_services_fastapi/0862_custom_pydantic_v2_validators_for_prompt_injection_patterns/README.md)
