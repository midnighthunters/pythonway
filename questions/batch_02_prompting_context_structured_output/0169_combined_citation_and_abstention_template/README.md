# Q0169 · Combined citation and abstention template

| Section | Topic | Difficulty |
|---|---|---|
| Prompting, Context Engineering & Structured Output | Grounding | Medium |

## Question

Design an output contract where the first line is `STATUS: answered` or `STATUS: not_found`, followed by the answer with citations. Write the parser that enforces it (answered replies must include at least one citation).

## Answer

```python
import re

CITE = re.compile(r"\[(\d+)\]")


def parse_grounded_reply(text: str, num_sources: int) -> dict:
    first, _, body = text.strip().partition("\n")
    m = re.fullmatch(r"STATUS:\s*(answered|not_found)", first.strip(), re.I)
    if not m:
        raise ValueError("missing STATUS line")
    status = m.group(1).lower()
    cites = sorted({int(n) for n in CITE.findall(body)})
    if status == "answered":
        if not cites:
            raise ValueError("answered without citations")
        if any(not 1 <= n <= num_sources for n in cites):
            raise ValueError(f"citation out of range: {cites}")
    return {"status": status, "answer": body.strip(), "citations": cites}


ok = parse_grounded_reply("STATUS: answered\nClaims go through Concur within 30 days [2].", 3)
assert ok == {"status": "answered", "answer": "Claims go through Concur within 30 days [2].", "citations": [2]}
assert parse_grounded_reply("STATUS: not_found\nI couldn't find this.", 3)["status"] == "not_found"
for bad in ("Claims go through Concur.", "STATUS: answered\nNo sources here.", "STATUS: answered\nSee [9]."):
    try:
        parse_grounded_reply(bad, 3)
        raise AssertionError(bad)
    except ValueError:
        pass
```

With structured outputs, the same contract is a schema with `status` and `citations` fields. The plain-text version is useful when you stream the answer to the UI while still getting a machine-checkable status.

## Likely follow-ups

- How would the UI behave differently for the two statuses?

---

[← Q0168](../../batch_02_prompting_context_structured_output/0168_compare_two_prompts_on_a_dev_set/README.md) · [Prompting, Context Engineering & Structured Output index](../README.md) · [All sections](../../README.md) · [Q0170 →](../../batch_02_prompting_context_structured_output/0170_extract_the_final_answer_from_tagged_output/README.md)
