
# Research Paper: Retrieval-Augmented Generation for Clinical Question Answering

## Abstract
We evaluated a RAG pipeline combining dense retrieval, cross-encoder reranking, and
large language models for clinical question answering. Our system achieved a 12% absolute
improvement in exact match accuracy over a standalone LLM baseline on a proprietary
medical QA dataset.

## Methods
- **Retriever:** OpenAI text-embedding-3-large, top-k=20.
- **Reranker:** BAAI/bge-reranker-large, top-n=6.
- **Generator:** GPT-4o-mini with system prompt enforcing citation use.
- **Dataset:** 2,500 clinical questions spanning internal medicine, pediatrics, and emergency medicine.

## Results
| Metric | LLM Only | RAG Pipeline |
|--------|----------|--------------|
| Exact Match | 34.2% | 46.8% |
| F1 Score | 41.5% | 53.7% |
| Citation Precision | N/A | 89.4% |
| Latency (P95) | 1.1s | 1.8s |

## Conclusion
RAG significantly improves accuracy and traceability for clinical QA. HyDE query rewriting
provided marginal gains on complex questions. Cross-encoder reranking was the highest-impact
component.
