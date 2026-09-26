# Q0185 · Chunked extraction over long documents

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Extraction | Medium |

## Question

You extract parties and attributes from a 200-page contract, chunk by chunk. Write the merge step: combine entities by normalised name and type, collect the pages they appear on, fill missing attributes, and record conflicting values instead of overwriting them.

## Answer

```python
def merge_entities(pages: list[list[dict]]) -> list[dict]:
    merged: dict[tuple[str, str], dict] = {}
    for page_no, entities in enumerate(pages, start=1):
        for e in entities:
            key = (e["type"], " ".join(e["name"].lower().split()))
            m = merged.setdefault(key, {"type": e["type"], "name": e["name"], "pages": [], "attrs": {}, "conflicts": []})
            m["pages"].append(page_no)
            for k, v in e.get("attrs", {}).items():
                if v is None:
                    continue
                if m["attrs"].get(k) is None:
                    m["attrs"][k] = v
                elif m["attrs"][k] != v:
                    m["conflicts"].append((k, m["attrs"][k], v, page_no))
    return list(merged.values())


pages = [
    [{"type": "party", "name": "Acme Ltd", "attrs": {"role": "supplier", "jurisdiction": None}}],
    [{"type": "party", "name": "ACME  Ltd", "attrs": {"jurisdiction": "England"}}],
    [{"type": "party", "name": "acme ltd", "attrs": {"jurisdiction": "Scotland"}}],
]
[acme] = merge_entities(pages)
assert acme["pages"] == [1, 2, 3] and acme["attrs"] == {"role": "supplier", "jurisdiction": "England"}
assert acme["conflicts"] == [("jurisdiction", "England", "Scotland", 3)]
```

Conflicts go to a reviewer, or to a focused second pass that sends both passages to the model. Never pick one silently. Overlapping chunks help catch entities split across boundaries, at the cost of more duplicates to merge.

## Likely follow-ups

- How would you handle entity aliases ("the Supplier" meaning Acme Ltd)?

---

[← Q0184](../../batch_02_prompting_context_structured_output/0184_extract_action_items_from_emails/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0186 →](../../batch_02_prompting_context_structured_output/0186_schema_evolution_for_structured_outputs/README.md)
