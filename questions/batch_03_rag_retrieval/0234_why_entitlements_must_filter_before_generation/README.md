# Q0234 · Why entitlements must filter before generation

| Section | Topic | Difficulty |
|---|---|---|
| Retrieval-Augmented Generation (RAG) | Security | Medium |

## Question

A teammate proposes retrieving from the whole corpus and then telling the model "only use documents the user may see". What's wrong with that?

## Answer

- The model will see restricted content. Once it's in the context, it can leak through the answer, paraphrase, summaries or refusals ("I can't tell you about the Project X layoffs"), and prompt injection can extract it deliberately.
- Instructions aren't access control. There's no guarantee of compliance, it isn't auditable, and it fails silently.
- Logs, traces and caches would store restricted content under the wrong user's request.
- It likely breaches need-to-know rules and information barriers (for example between private-side deal teams and public-side research), which is a regulatory issue, not just a bug.

Correct design: authenticate the user, resolve their entitlements, filter at the retrieval layer (and again at tool calls), and log which documents were used. Then generate only from permitted content. Test it with an entitlement evaluation suite: users with different roles asking for restricted information, where the expected result is no leak.

## Likely follow-ups

- How would you build an automated test suite for entitlement leaks?

---

[← Q0233](../../batch_03_rag_retrieval/0233_entitlement_aware_retrieval/README.md) · [Retrieval-Augmented Generation (RAG) index](../README.md) · [All sections](../../README.md) · [Q0235 →](../../batch_03_rag_retrieval/0235_information_barriers_in_rag/README.md)
