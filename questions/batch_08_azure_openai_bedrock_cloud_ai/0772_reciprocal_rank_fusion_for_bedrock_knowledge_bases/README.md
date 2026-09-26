# Q0772 · Reciprocal Rank Fusion for Bedrock Knowledge Bases

| Section | Topic | Difficulty |
|---|---|---|
| Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure | AWS Bedrock | Medium |

## Question

Write Python code implementing Reciprocal Rank Fusion (RRF) to merge and rerank two ranked result lists from vector search and BM25 search.

## Answer

Reciprocal Rank Fusion (RRF) is an unsupervised ranking algorithm that merges rankings from diverse retrieval mechanisms without requiring calibrated score normalization.

Formula:
$RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$
where $k$ is a constant (typically 60) and $r_m(d)$ is the 1-based rank position of document $d$ in system $m$.

```python
from typing import Dict, List, Tuple


def reciprocal_rank_fusion(
    ranked_lists: List[List[str]], k: int = 60
) -> List[Tuple[str, float]]:
    scores: Dict[str, float] = {}

    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list, start=1):
            if doc_id not in scores:
                scores[doc_id] = 0.0
            scores[doc_id] += 1.0 / (k + rank)

    # Sort descending by fused score
    sorted_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_docs


vector_results = ["doc_B", "doc_A", "doc_C"]
bm25_results = ["doc_B", "doc_D", "doc_A"]

fused = reciprocal_rank_fusion([vector_results, bm25_results], k=60)
assert fused[0][0] == "doc_B"
assert fused[0][1] > fused[1][1]
```

## Likely follow-ups

- Why does RRF use constant $k=60$ rather than $k=0$?
- How does RRF compare to cross-encoder reranking models (e.g. Cohere Rerank)?

---

[← Q0771](../../batch_08_azure_openai_bedrock_cloud_ai/0771_knowledge_bases_hybrid_search_bm25_plus_opensearch_vector/README.md) · [Azure OpenAI, AWS Bedrock & Cloud AI Infrastructure index](../README.md) · [All sections](../../README.md) · [Q0773 →](../../batch_08_azure_openai_bedrock_cloud_ai/0773_bedrock_agents_action_group_lambda_implementation/README.md)
