# Research Paper: Retrieval-Augmented Generation for Healthcare Knowledge Systems

**Authors:** Aisha Patel¹, Dr. James Worthington², Dr. Li Wei³
**Institutions:** ¹HealthTech AI Lab, ²Stanford Medical Informatics, ³MIT CSAIL
**Published:** HealthTech Internal Research Report, January 2025
**Access Tags:** all-employees

---

## Abstract

Retrieval-Augmented Generation (RAG) has emerged as a promising paradigm for grounding
large language model (LLM) outputs in verifiable source documents, thereby reducing hallucinations
in high-stakes clinical and enterprise settings. This paper presents a comprehensive empirical
evaluation of RAG system configurations for healthcare knowledge management, comparing embedding
models, chunking strategies, and reranking algorithms on a proprietary benchmark of 2,400
clinical and administrative question-answer pairs. Our findings show that a hybrid pipeline
using domain-fine-tuned embeddings, semantic chunking at 300-token windows with 30-token overlap,
and cross-encoder reranking achieves a hallucination rate of 0.8% and answer F1 of 0.84 on the
held-out test set, outperforming vanilla RAG by 18% on factuality metrics.

---

## 1. Introduction

Healthcare enterprises face a dual challenge when deploying conversational AI systems: (1) the
need for accurate, evidence-grounded answers that meet clinical and regulatory standards, and
(2) the strict privacy and access-control requirements imposed by HIPAA, GDPR, and internal
data governance policies. Classic LLM approaches without retrieval augmentation suffer from
hallucination rates of 5–15% on specialized domain questions [1], which is unacceptable in
clinical settings where erroneous recommendations can lead to patient harm.

RAG addresses this by confining the LLM's generation to a retrieved context window, limiting
the model's ability to confabulate unsupported facts. However, the quality of the retrieval
stage critically determines the quality of the final answer. A retriever that misses relevant
passages will cause the LLM to produce incomplete or incorrect responses even if the LLM itself
is well-calibrated.

This paper investigates the design space of RAG systems specifically for healthcare enterprise
use cases, including administrative HR queries, clinical protocol questions, and product
documentation lookups.

---

## 2. System Design

### 2.1 Embedding Models Evaluated

| Model | Dimensions | Avg Recall@10 |
|-------|-----------|-------------|
| OpenAI text-embedding-3-large | 3072 | 0.89 |
| OpenAI text-embedding-3-small | 1536 | 0.84 |
| MedBERT-Large (fine-tuned) | 1024 | 0.92 |
| BGE-M3 | 1024 | 0.87 |
| all-mpnet-base-v2 | 768 | 0.79 |

Fine-tuned MedBERT-Large achieves the highest recall on clinical queries.
OpenAI text-embedding-3-large is the best general-purpose option without fine-tuning.

### 2.2 Chunking Strategies

| Strategy | Chunk Size | Overlap | Answer F1 |
|---------|-----------|--------|----------|
| Fixed-size | 512 tokens | 0 | 0.71 |
| Fixed-size + overlap | 300 tokens | 50 tokens | 0.76 |
| Semantic (heading + paragraph) | 200-400 tokens | 30 tokens | 0.84 |
| Sentence-level | ~50 tokens | 0 | 0.68 |

Semantic chunking at 200–400 tokens with 30-token overlap yields the best answer quality.
This aligns with natural document structure (sections, paragraphs) and reduces mid-sentence breaks
that degrade coherence.

### 2.3 Reranking

| Reranker | Precision@5 | Latency Overhead |
|---------|------------|----------------|
| None (cosine only) | 0.61 | 0ms |
| bge-reranker-base | 0.74 | +120ms |
| bge-reranker-large | 0.81 | +280ms |
| ClinicalReranker (fine-tuned) | 0.86 | +310ms |

Cross-encoder reranking adds 120–310ms overhead but improves precision by 25–41%.
The overhead is acceptable for p95 latency targets up to 2s.

---

## 3. Evaluation Methodology

### 3.1 Benchmark Construction

A golden evaluation set of 2,400 question-answer pairs was constructed by domain experts:
- 800 clinical protocol questions (treatment guidelines, drug interactions)
- 600 administrative questions (HR policies, IT security, onboarding)
- 500 product documentation questions (API specs, model performance)
- 500 adversarial questions (out-of-scope, hallucination-probing)

### 3.2 Metrics

- **Recall@K:** Fraction of queries where the correct document chunk appears in top-K results.
- **MRR (Mean Reciprocal Rank):** Measures ranking quality of the first correct result.
- **Answer F1:** Token-level F1 between generated answer and reference answer.
- **Hallucination Rate:** Fraction of answers containing claims not supported by retrieved context
  (scored by GPT-4o as judge).
- **Latency:** p50, p95, p99 end-to-end from query to response.

---

## 4. Results

### 4.1 Main Results

| System | Recall@10 | MRR | Answer F1 | Hallucination Rate | p95 Latency |
|--------|----------|-----|----------|-------------------|------------|
| Vanilla LLM (no RAG) | – | – | 0.61 | 12.3% | 890ms |
| RAG + fixed-size chunks | 0.79 | 0.64 | 0.71 | 4.1% | 1,240ms |
| RAG + semantic chunks | 0.86 | 0.73 | 0.79 | 2.2% | 1,310ms |
| RAG + semantic + rerank | 0.91 | 0.82 | 0.84 | 0.8% | 1,620ms |
| RAG + fine-tuned embed + rerank | 0.94 | 0.87 | 0.87 | 0.5% | 1,680ms |

### 4.2 Adversarial Robustness

On the 500 adversarial queries (out-of-scope or unanswerable questions):
- The best system correctly abstained ("I don't have enough information") in 91% of cases.
- Baseline vanilla LLM hallucinated a plausible-sounding but incorrect answer in 68% of cases.

---

## 5. Conclusions

1. Semantic chunking at 200–400 tokens with overlap is the single highest-impact design choice.
2. Cross-encoder reranking reduces hallucination rate by 60–80% compared to cosine-only retrieval.
3. Domain-specific embedding fine-tuning provides an additional 3–5% improvement in factuality.
4. The production-ready RAG system (semantic chunks + bge-reranker-large + GPT-4o-mini) achieves
   a hallucination rate of 0.8% and p95 latency of 1,620ms, meeting the <2s SLA.

---

## References

[1] Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization. ACL 2020.
[2] Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020.
[3] Xiong et al. (2024). MedRAG: Towards Medical Retrieval-Augmented Generation. arXiv:2402.09970.
[4] Gao et al. (2023). Precise Zero-Shot Dense Retrieval without Relevance Labels (HyDE). ACL 2023.
