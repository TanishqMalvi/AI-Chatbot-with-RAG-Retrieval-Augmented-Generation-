
# Product Specification v2.0

**Owner:** Product Management | **Status:** Released

## Summary
HealthTech RAG Assistant v2.0 introduces multi-tenant retrieval, HyDE query rewriting, and
cross-encoder reranking to improve answer relevance and reduce hallucination.

## Features
### Multi-Tenant Retrieval
- Documents tagged with `access_tags` and `pii_flags`.
- Queries filtered by user role at retrieval time.
- Supports row-level ACL without custom code per tenant.

### Query Rewriting
- **HyDE:** generate hypothetical answer to improve vector similarity.
- **Multi-query:** expand user query into 3 semantically diverse queries.
- Configurable strategy per request: `none`, `hyde`, `multi_query`, `both`.

### Reranking
- Cross-encoder model: `cross-encoder/ms-marco-MiniLM-L-6-v2`.
- Rerank top-20 candidates to top-6 final chunks.
- Latency budget: add ~40 ms per query.

### Guardrails
- Input: PII redaction + prompt injection detection.
- Output: confidence scoring + citation enforcement + optional hallucination check.

## Non-Functional Requirements
- P95 latency: < 2 seconds for end-to-end chat.
- Availability: 99.9% uptime excluding planned maintenance.
- Data retention: audit logs 6 years; embeddings retained indefinitely unless deleted by tenant.
