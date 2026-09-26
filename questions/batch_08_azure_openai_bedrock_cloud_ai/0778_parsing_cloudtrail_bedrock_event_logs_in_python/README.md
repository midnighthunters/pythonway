# Q0778 · Parsing CloudTrail Bedrock event logs in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Write Python code that parses simulated AWS CloudTrail Bedrock event logs and extracts unauthorized invocation attempts (access denied / 403).

## Answer

```python
from typing import Any, Dict, List


class CloudTrailAuditAnalyzer:
    @staticmethod
    def extract_security_incidents(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        incidents = []
        for ev in events:
            error_code = ev.get("errorCode")
            if error_code in {"AccessDenied", "Client.UnauthorizedException"}:
                incidents.append({
                    "time": ev.get("eventTime"),
                    "principal": ev.get("userIdentity", {}).get("arn"),
                    "model": ev.get("requestParameters", {}).get("modelId"),
                    "source_ip": ev.get("sourceIPAddress"),
                    "reason": ev.get("errorMessage"),
                })
        return incidents


audit_events = [
    {
        "eventTime": "2026-09-26T14:00:00Z",
        "eventName": "InvokeModel",
        "userIdentity": {"arn": "arn:aws:iam::123:role/analyst-role"},
        "requestParameters": {"modelId": "anthropic.claude-3-5-sonnet"},
        "sourceIPAddress": "10.100.4.2",
    },
    {
        "eventTime": "2026-09-26T14:02:10Z",
        "eventName": "InvokeModel",
        "errorCode": "AccessDenied",
        "errorMessage": "User is not authorized to perform: bedrock:InvokeModel",
        "userIdentity": {"arn": "arn:aws:iam::123:role/unauthorized-intern"},
        "requestParameters": {"modelId": "anthropic.claude-3-opus"},
        "sourceIPAddress": "192.168.1.50",
    },
]

violations = CloudTrailAuditAnalyzer.extract_security_incidents(audit_events)
assert len(violations) == 1
assert violations[0]["principal"] == "arn:aws:iam::123:role/unauthorized-intern"
assert violations[0]["model"] == "anthropic.claude-3-opus"
```

## Likely follow-ups

- How can Amazon EventBridge trigger automated security isolation when an `AccessDenied` alert fires?
- How do SIEM platforms (Splunk, Microsoft Sentinel) ingest CloudTrail streams via SQS/Kinesis?

---

[← Q0777](../../batch_08_azure_openai_bedrock_cloud_ai/0777_bedrock_cloudtrail_event_logging_for_compliance_audits/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0779 →](../../batch_08_azure_openai_bedrock_cloud_ai/0779_cross_region_inference_profile_latency_monitoring/README.md)
