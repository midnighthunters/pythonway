# Q0456 · Transactional outbox for agent side effects

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Reliability | Hard |

## Question

An agent step must update its state and send a notification atomically. Implement the transactional outbox pattern with SQLite: write the state change and an outbox row in one transaction, then a relay publishes pending rows and marks them sent.

## Answer

```python
import json
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE runs(run_id TEXT PRIMARY KEY, status TEXT);
CREATE TABLE outbox(id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT, payload TEXT, sent INTEGER DEFAULT 0);
INSERT INTO runs VALUES ('run-1', 'running');
""")


def complete_step(run_id: str, fail_after_update: bool = False) -> None:
    with db:
        db.execute("UPDATE runs SET status = 'rebooked' WHERE run_id = ?", (run_id,))
        if fail_after_update:
            raise RuntimeError("crash mid-transaction")
        db.execute("INSERT INTO outbox(topic, payload) VALUES (?, ?)",
                   ("notifications", json.dumps({"run_id": run_id, "msg": "You're rebooked on LH903"})))


def relay(publish) -> int:
    rows = db.execute("SELECT id, topic, payload FROM outbox WHERE sent = 0 ORDER BY id").fetchall()
    for row_id, topic, payload in rows:
        publish(topic, json.loads(payload))
        with db:
            db.execute("UPDATE outbox SET sent = 1 WHERE id = ?", (row_id,))
    return len(rows)


try:
    complete_step("run-1", fail_after_update=True)
except RuntimeError:
    pass
assert db.execute("SELECT status FROM runs").fetchone() == ("running",)
complete_step("run-1")
published: list = []
assert relay(lambda t, p: published.append((t, p))) == 1 and relay(lambda t, p: published.append((t, p))) == 0
assert published == [("notifications", {"run_id": "run-1", "msg": "You're rebooked on LH903"})]
```

The crashed attempt rolled back both writes: no state change without its notification, and vice versa. The relay gives at-least-once delivery (a crash between publish and marking sent means a resend), so consumers deduplicate by outbox id. At scale, change-data-capture (Debezium) can replace the polling relay.

## Likely follow-ups

- Why not just send the notification directly after committing the state?

---

[← Q0455](../../batch_05_agentic_patterns_orchestration/0455_optimistic_concurrency_for_agent_writes/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0457 →](../../batch_05_agentic_patterns_orchestration/0457_escalate_to_a_human_with_context/README.md)
