# Q0727 · Simulating PagedAttention block table allocation in Python

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | GPU Serving | Hard |

## Question

Write Python code that simulates a PagedAttention memory manager, allocating fixed-size physical blocks for incoming sequences and releasing them upon completion.

## Answer

```python
from typing import Dict, List, Optional


class PagedAttentionMemoryManager:
    def __init__(self, total_blocks: int, block_size: int = 16):
        self.block_size = block_size
        self.free_blocks: List[int] = list(range(total_blocks))
        # Maps sequence_id -> list of physical block numbers
        self.block_tables: Dict[str, List[int]] = {}

    def allocate_token(self, seq_id: str, current_token_count: int) -> bool:
        if seq_id not in self.block_tables:
            self.block_tables[seq_id] = []

        # Check if we need a new block
        if current_token_count % self.block_size == 1 or current_token_count == 1:
            if not self.free_blocks:
                return False  # Out of GPU memory
            new_block = self.free_blocks.pop(0)
            self.block_tables[seq_id].append(new_block)
        return True

    def free_sequence(self, seq_id: str) -> None:
        if seq_id in self.block_tables:
            blocks = self.block_tables.pop(seq_id)
            self.free_blocks.extend(blocks)


mgr = PagedAttentionMemoryManager(total_blocks=10, block_size=4)
# Sequence 1 generates 5 tokens: requires 2 blocks (tokens 1-4 in block 0, token 5 in block 1)
for t in range(1, 6):
    assert mgr.allocate_token("seq-1", t) is True

assert len(mgr.block_tables["seq-1"]) == 2
assert len(mgr.free_blocks) == 8

# Free sequence
mgr.free_sequence("seq-1")
assert len(mgr.free_blocks) == 10
assert "seq-1" not in mgr.block_tables
```

## Likely follow-ups

- How does the manager handle preemption when memory is exhausted mid-generation?
- How is prefix sharing implemented when two sequences share an identical initial prompt?

---

[← Q0726](../../batch_08_azure_openai_bedrock_cloud_ai/0726_pagedattention_and_kv_cache_memory_allocation/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0728 →](../../batch_08_azure_openai_bedrock_cloud_ai/0728_gpu_quantization_fp8_awq_gptq_int4_for_enterprise_inference/README.md)
