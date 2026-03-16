# HealthTech ClinicalAI Platform – Product Specification v2.0

**Status:** Beta | **Target GA:** Q3 2025
**Product Owner:** Dr. Priya Sharma | **Engineering Lead:** Keiko Tanaka
**Access Tags:** all-employees

---

## 1. What's New in v2.0

ClinicalAI v2.0 introduces a Retrieval-Augmented Generation (RAG) layer on top of the v1.0
probabilistic ML models, enabling:

- **Natural language clinical queries** by physicians (e.g., "What are the treatment options
  for this patient's combination of HFpEF and CKD Stage 3?")
- **Evidence citations** from UpToDate, PubMed, and internal clinical guidelines.
- **Multimodal inputs:** Structured EHR data + free-text clinical notes + radiology reports.
- **Conversation continuity:** Multi-turn clinical dialogue maintained per encounter session.

---

## 2. New Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ClinicalAI v2.0                       │
│                                                         │
│  EHR Structured ──►  Feature Extractor                  │
│  Clinical Notes ──►  MedBERT Embedder ──► Vector Store  │
│  Radiology TXT  ──►                         │           │
│                                             ▼           │
│  Physician Query ──► Query Rewriter ──► Retriever       │
│                                             │           │
│                                        Reranker         │
│                                             │           │
│                                        GPT-4o + RAG     │
│                                             │           │
│                                    Clinical Guardrails  │
│                                             │           │
│                                      Recommendation     │
└─────────────────────────────────────────────────────────┘
```

---

## 3. New Models

### 3.1 MedBERT-Large Embedder

Fine-tuned on PubMed abstracts + MIMIC-III clinical notes.
- Embedding dimension: 1024
- Max sequence length: 512 tokens
- Outperforms text-embedding-3-large on clinical retrieval benchmarks by +8% nDCG@10.

### 3.2 ClinicalReranker v1

Cross-encoder fine-tuned on MedQA + clinical query-document pairs.
- 23% improvement in Precision@5 vs. bge-reranker-large on clinical retrieval.

### 3.3 Generation

- Primary: GPT-4o with clinical system prompt.
- Fallback: Claude 3.5 Sonnet (lower latency in high-load scenarios).
- Clinical guardrails: Every recommendation includes evidence citations and confidence scores.
- Dosing recommendations are flagged for pharmacist review before display.

---

## 4. Multimodal Inputs

| Input Type | Processing |
|-----------|-----------|
| EHR structured data | Direct featurization (FHIR → JSON) |
| Clinical notes (free text) | MedBERT tokenization + chunking (256-token chunks) |
| Radiology reports | Layout-aware PDF extraction → MedBERT |
| Lab results | Time-series normalization → tabular features |

---

## 5. Compliance Changes

- **FDA:** Pre-submission meeting completed for De Novo pathway (AI/ML SaMD).
- **Transparency:** v2.0 includes an explanation layer showing which retrieved passages drove
  each recommendation, meeting EU AI Act Article 13 transparency requirements.
- **Audit trail:** Every query, retrieved chunk, model version, and clinician action is logged
  with immutable timestamps to an append-only audit log (AWS QLDB).

---

## 6. Performance Targets

| Metric | Target |
|--------|--------|
| End-to-end p95 latency | < 2.0s |
| Answer factuality (LLM judge) | ≥ 95% |
| Citation coverage | 100% (every claim cited) |
| Hallucination rate | < 1% |

---

## 7. Migration Path from v1.0

1. Deploy v2.0 API alongside v1.0 (blue-green).
2. Route 10% of traffic to v2.0 via feature flag.
3. Monitor latency, accuracy, and clinical staff satisfaction (NPS).
4. Ramp to 100% over 8 weeks.
5. Maintain v1.0 in hot standby for 90 days post-migration.

---

## 8. Open Issues

- [ ] Pediatric dosing guardrails (target: GA)
- [ ] Non-English language support (target: Q4 2025)
- [ ] Integration with voice-dictation workflows (target: 2026)
