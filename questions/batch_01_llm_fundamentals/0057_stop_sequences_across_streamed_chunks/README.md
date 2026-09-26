# Q0057 · Stop sequences across streamed chunks

| Section | Topic | Difficulty |
|---|---|---|
| LLM Fundamentals & Inference | Streaming | Medium |

## Question

Implement a stop-sequence filter for a token stream. It must emit text as early as possible, never emit any part of a stop sequence, and handle a stop sequence split across chunks.

## Answer

Approach: buffer only the longest suffix that could still be the start of a stop sequence, and emit the rest. When a full stop sequence appears, emit the text before it and finish.

```python
class StopFilter:
    def __init__(self, stops: list[str]) -> None:
        self.stops = [s for s in stops if s]
        self.hold = max((len(s) for s in self.stops), default=1) - 1
        self.buf = ""
        self.done = False

    def feed(self, chunk: str) -> str:
        if self.done:
            return ""
        self.buf += chunk
        hits = [i for i in (self.buf.find(s) for s in self.stops) if i != -1]
        if hits:
            out, self.buf, self.done = self.buf[:min(hits)], "", True
            return out
        keep = 0
        for k in range(min(self.hold, len(self.buf)), 0, -1):
            if any(s.startswith(self.buf[-k:]) for s in self.stops):
                keep = k
                break
        out, self.buf = self.buf[:len(self.buf) - keep], self.buf[len(self.buf) - keep:]
        return out

    def flush(self) -> str:
        out = "" if self.done else self.buf
        self.buf = ""
        return out


f = StopFilter(["\nUser:"])
assert [f.feed(c) for c in ["Hello", " world\nUs", "er: hi"]] == ["Hello", " world", ""]
assert f.done and f.flush() == ""
g = StopFilter(["XYZ"])
assert g.feed("abc") == "abc" and g.feed("dX") == "d" and g.feed("Y") == "" and g.feed("Q") == "XYQ"
assert g.flush() == ""
h = StopFilter(["END"])
assert h.feed("almost E") == "almost " and h.flush() == "E"
```

Held-back text is released as soon as it can no longer match, so users see no visible stall. Providers apply stop sequences server-side, but you need this for your own sentinels, for example to stop at `</answer>` or before a leaked tool-call marker.

## Likely follow-ups

- How would you do this efficiently for hundreds of stop sequences (Aho-Corasick)?

---

[← Q0056](../../batch_01_llm_fundamentals/0056_render_a_chat_template_safely/README.md) · [LLM Fundamentals & Inference index](../README.md) · [All sections](../../README.md) · [Q0058 →](../../batch_01_llm_fundamentals/0058_sources_of_non_determinism_in_llm_apis/README.md)
