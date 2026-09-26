# Q0971 · Optical Character Recognition PII scrubbing from uploaded document scans

| Section | Topic | Difficulty |
|---|---|---|
| AI Security, Guardrails & Responsible AI in a Bank | PII and DLP | Medium |

## Question

Write Python code implementing a document image text-bounding-box PII scrubber that identifies PII in OCR output and calculates redacted bounding boxes.

## Answer

When processing scanned checks, passports, or tax returns, visual PII must be scrubbed from the image before sharing or archiving. The scrubber takes bounding boxes of recognized words, matches PII patterns, and flags the pixel coordinates for black-box redaction.

```python
import re
from typing import Dict, List, Tuple


class BoundingBoxPIIScrubber:
    @staticmethod
    def identify_pii_boxes(ocr_words: List[Dict]) -> List[Dict]:
        """ocr_words: list of dicts with keys 'word', 'bbox': [x1, y1, x2, y2]."""
        pii_boxes = []
        ssn_pattern = re.compile(r"^\d{3}-\d{2}-\d{4}$")

        for item in ocr_words:
            if ssn_pattern.match(item["word"]):
                pii_boxes.append({
                    "word": item["word"],
                    "redact_bbox": item["bbox"],
                    "entity_type": "SSN",
                })
        return pii_boxes


ocr_output = [
    {"word": "Form", "bbox": [10, 10, 50, 30]},
    {"word": "W-2", "bbox": [55, 10, 85, 30]},
    {"word": "123-45-6789", "bbox": [100, 50, 200, 75]},
]

redaction_targets = BoundingBoxPIIScrubber.identify_pii_boxes(ocr_output)
assert len(redaction_targets) == 1
assert redaction_targets[0]["entity_type"] == "SSN"
assert redaction_targets[0]["redact_bbox"] == [100, 50, 200, 75]
```

## Likely follow-ups

- How does OpenCV or Pillow draw solid black rectangles over redacted bounding boxes?
- What are the risks of OCR misrecognizing a character (e.g. 'O' vs '0') and failing regex matching?

---

[← Q0970](../../batch_10_ai_security_responsible_ai/0970_redacting_sensitive_connection_strings_and_secrets_from/README.md) · [AI Security, Guardrails & Responsible AI in a Bank index](../README.md) · [All sections](../../README.md) · [Q0972 →](../../batch_10_ai_security_responsible_ai/0972_audio_transcript_pii_masking_in_call_center_voice_agents/README.md)
