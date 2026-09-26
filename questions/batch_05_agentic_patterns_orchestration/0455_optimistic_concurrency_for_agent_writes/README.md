# Q0455 · Optimistic concurrency for agent writes

| Section | Topic | Difficulty |
|---|---|---|
| Agentic Patterns & Orchestration | Concurrency | Medium |

## Question

Implement optimistic concurrency control for an agent that edits a shared document or record: writes include the version they read, conflicting writes are rejected, and the agent re-reads and retries.

## Answer

```python
class VersionConflict(Exception):
    pass


class Store:
    def __init__(self) -> None:
        self.data = {"doc-1": {"version": 1, "text": "Draft v1"}}

    def read(self, key: str) -> dict:
        return dict(self.data[key])

    def write(self, key: str, text: str, expected_version: int) -> int:
        cur = self.data[key]
        if cur["version"] != expected_version:
            raise VersionConflict(f"expected v{expected_version}, found v{cur['version']}")
        self.data[key] = {"version": cur["version"] + 1, "text": text}
        return cur["version"] + 1


def agent_update(store: Store, key: str, edit, retries: int = 3) -> int:
    for _ in range(retries):
        snapshot = store.read(key)
        try:
            return store.write(key, edit(snapshot["text"]), snapshot["version"])
        except VersionConflict:
            continue
    raise RuntimeError("gave up after repeated conflicts")


s = Store()
snapshot = s.read("doc-1")
s.write("doc-1", "Draft v1 + human edit", 1)
try:
    s.write("doc-1", "agent overwrite", snapshot["version"])
    raise AssertionError
except VersionConflict:
    pass
new_version = agent_update(s, "doc-1", lambda t: t + " + agent summary")
assert new_version == 3 and s.read("doc-1")["text"] == "Draft v1 + human edit + agent summary"
```

The agent's first write would have silently erased a human's edit. With versioning it re-reads and applies its change on top. HTTP APIs express this with ETags and `If-Match`, and databases with a version column in the `WHERE` clause. Re-run the model step on the fresh content if the edit depends on it.

## Likely follow-ups

- When is optimistic concurrency a bad fit?

---

[← Q0454](../../batch_05_agentic_patterns_orchestration/0454_locks_when_agents_share_resources/README.md) · [Agentic Patterns & Orchestration index](../README.md) · [All sections](../../README.md) · [Q0456 →](../../batch_05_agentic_patterns_orchestration/0456_transactional_outbox_for_agent_side_effects/README.md)
