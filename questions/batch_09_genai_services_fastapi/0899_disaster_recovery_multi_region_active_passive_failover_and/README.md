# Q0899 · Disaster recovery: multi-region active-passive failover and DNS routing

| Section | Topic | Difficulty |
|---|---|---|
| Building GenAI Services: FastAPI, Streaming, Queues & NoSQL | Containers and deployment | Medium |

## Question

Explain disaster recovery (DR) architectures for enterprise GenAI platforms using AWS Route 53 / Azure Traffic Manager, and write Python code simulating health-check driven DNS failover.

## Answer

If a primary cloud region (`us-east-1`) suffers an outage:
1. **Health Check Probes**: Route 53 or Traffic Manager continuously probes the primary region's `/readyz` endpoint.
2. **Automated Failover**: When consecutive failures exceed the threshold, DNS updates the endpoint record to route all incoming global traffic to the secondary active-passive region (`us-west-2`).
3. **Data Replication**: Cold/warm standby regions rely on replicated NoSQL conversation tables and synchronized vector indexes.

```python
from typing import Dict, List


class DNSHealthCheckFailoverRouter:
    def __init__(self, primary_url: str, secondary_url: str, failure_threshold: int = 3):
        self.primary_url = primary_url
        self.secondary_url = secondary_url
        self.failure_threshold = failure_threshold
        self.primary_consecutive_failures = 0

    def record_probe(self, is_primary_healthy: bool) -> None:
        if is_primary_healthy:
            self.primary_consecutive_failures = 0
        else:
            self.primary_consecutive_failures += 1

    def resolve_dns_target(self) -> str:
        if self.primary_consecutive_failures >= self.failure_threshold:
            return self.secondary_url  # Failover to DR region
        return self.primary_url


router = DNSHealthCheckFailoverRouter(
    primary_url="https://us-east.llmsuite.jpmc.com",
    secondary_url="https://us-west.llmsuite.jpmc.com",
    failure_threshold=3,
)

# Initially routes to primary
assert router.resolve_dns_target() == "https://us-east.llmsuite.jpmc.com"

# Primary fails 3 consecutive probes
router.record_probe(False)
router.record_probe(False)
router.record_probe(False)

# Routes to DR secondary region
assert router.resolve_dns_target() == "https://us-west.llmsuite.jpmc.com"
```

## Likely follow-ups

- What is DNS TTL caching, and how does client DNS caching delay effective failover?
- What are Recovery Point Objective (RPO) and Recovery Time Objective (RTO) targets in Tier-1 banking applications?

---

[← Q0898](../../batch_09_genai_services_fastapi/0898_network_policies_and_private_egress_via_corporate_forward/README.md) · [Building GenAI Services: FastAPI, Streaming, Queues & NoSQL index](../README.md) · [All sections](../../README.md) · [Q0900 →](../../batch_09_genai_services_fastapi/0900_complete_production_architecture_review_end_to_end_design/README.md)
