# Q0347 · Test streaming handlers against arbitrary chunking

| Section | Topic | Difficulty |
|---|---|---|
| LLM Evaluation, Testing & Observability | Testing | Medium |

## Question

Network chunks can split lines and even multi-byte UTF-8 characters anywhere. Write a line assembler for a streamed byte protocol and test it by splitting the stream at every possible point.

## Answer

```python
import codecs
import random


class LineAssembler:
    def __init__(self) -> None:
        self._decoder = codecs.getincrementaldecoder("utf-8")()
        self._buf = ""

    def feed(self, chunk: bytes) -> list[str]:
        self._buf += self._decoder.decode(chunk)
        *lines, self._buf = self._buf.split("\n")
        return lines

    def close(self) -> list[str]:
        self._buf += self._decoder.decode(b"", final=True)
        rest, self._buf = self._buf, ""
        return [rest] if rest else []


payload = 'data: {"t": "Café £5"}\ndata: {"t": "😀 done"}\n'.encode()
expected = ['data: {"t": "Café £5"}', 'data: {"t": "😀 done"}']

for i in range(len(payload) + 1):
    for j in range(i, len(payload) + 1):
        la = LineAssembler()
        got = la.feed(payload[:i]) + la.feed(payload[i:j]) + la.feed(payload[j:]) + la.close()
        assert got == expected, (i, j)

rng = random.Random(3)
for _ in range(200):
    la, got, pos = LineAssembler(), [], 0
    while pos < len(payload):
        step = rng.randint(1, 5)
        got += la.feed(payload[pos:pos + step])
        pos += step
    assert got + la.close() == expected
```

The incremental decoder holds partial UTF-8 sequences across chunks. Naively calling `chunk.decode()` would raise or corrupt "é", "£" and emoji. Exhaustive split testing is cheap here and catches the boundary bugs that only show up in production under certain network conditions.

## Likely follow-ups

- How would you extend this to parse SSE events (multi-line `data:` fields, blank-line terminators)?

---

[← Q0346](../../batch_04_llm_evaluation_observability/0346_contract_tests_for_provider_adapters/README.md) · [LLM Evaluation, Testing & Observability index](../README.md) · [All sections](../../README.md) · [Q0348 →](../../batch_04_llm_evaluation_observability/0348_metamorphic_testing_for_llm_systems/README.md)
