# HealthTech RAG Assistant

> **Production-grade Retrieval-Augmented Generation chatbot** for HealthTech Inc. enterprise
> knowledge management. Answers employee questions about policies, products, HR guidelines,
> and research papers with JWT-based RBAC, row-level ACLs, PII redaction, and hallucination
> guardrails.

[![CI](https://github.com/TanishqMalvi/AI-Chatbot-with-RAG-Retrieval-Augmented-Generation-/actions/workflows/ci.yml/badge.svg)](https://github.com/TanishqMalvi/AI-Chatbot-with-RAG-Retrieval-Augmented-Generation-/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Table of Contents

1. [Architecture](#architecture)
2. [Quick Start](#quick-start)
3. [Configuration](#configuration)
4. [API Reference](#api-reference)
5. [Document Ingestion](#document-ingestion)
6. [Security & Compliance](#security--compliance)
7. [Evaluation](#evaluation)
8. [Production Deployment](#production-deployment)
9. [Blueprint Compliance](#blueprint-compliance)
10. [Future: Agentic Extension](#future-agentic-extension)

---

## Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    RAG Pipeline (Blueprint §15)                     │
│                                                                    │
│  User Query                                                        │
│      │                                                             │
│      ▼                                                             │
│  ┌─────────────┐    PII redaction + injection detection            │
│  │ Input Guard │────────────────────────────────────────────────►  │
│  └─────────────┘                                                   │
│      │                                                             │
│      ▼                                                             │
│  ┌──────────────────┐   HyDE / multi-query expansion               │
│  │  Query Rewriter  │────────────────────────────────────────────► │
│  └──────────────────┘                                              │
│      │                                                             │
│      ▼                                                             │
│  ┌──────────────────────────────────────┐                          │
│  │  Vector Retrieval (Chroma / Pinecone) │  ACL filter pre-applied │
│  │  top-k=20, cosine similarity          │                         │
│  └──────────────────────────────────────┘                          │
│      │                                                             │
│      ▼                                                             │
│  ┌────────────────────────────┐                                    │
│  │  Cross-Encoder Reranker    │  bge-reranker-large → top-5/8     │
│  └────────────────────────────┘                                    │
│      │                                                             │
│      ▼                                                             │
│  ┌────────────────────────┐                                        │
│  │  LLM Generation        │  GPT-4o-mini (default)                │
│  │  (system prompt + ctx) │  Claude 3.5 Sonnet (fallback)         │
│  └────────────────────────┘                                        │
│      │                                                             │
│      ▼                                                             │
│  ┌──────────────────────────────────────────┐                      │
│  │  Output Guard                             │                     │
│  │  • Confidence threshold check             │                     │
│  │  • Citation enforcement                   │                     │
│  │  • LLM-as-judge hallucination detection   │                     │
│  └──────────────────────────────────────────┘                      │
│      │                                                             │
│      ▼                                                             │
│  Structured Response (answer + sources + confidence + latency)     │
└────────────────────────────────────────────────────────────────────┘
```

### Stack

| Component | Technology |
|-----------|-----------|
| **API** | FastAPI 0.115 + Uvicorn |
| **Orchestration** | LangChain 0.3 |
| **Embeddings** | OpenAI text-embedding-3-large (fallback: 3-small) |
| **Vector DB (dev)** | Chroma (local, persistent) |
| **Vector DB (prod)** | Pinecone Serverless (one env-var switch) |
| **Reranker** | BAAI/bge-reranker-large (cross-encoder) |
| **LLM default** | GPT-4o-mini |
| **LLM fallback** | Claude 3.5 Sonnet |
| **Caching** | Redis 7 |
| **Auth** | JWT (HS256) |
| **PII redaction** | Microsoft Presidio |
| **Observability** | LangSmith / OpenTelemetry |
| **Deployment** | Docker + docker-compose (dev), Kubernetes (prod) |
| **CI/CD** | GitHub Actions with eval regression gate |

---

## Quick Start

### 1. Prerequisites

- Python 3.11+
- Docker & docker-compose
- OpenAI API key

### 2. Clone & configure

```bash
git clone https://github.com/TanishqMalvi/AI-Chatbot-with-RAG-Retrieval-Augmented-Generation-.git
cd AI-Chatbot-with-RAG-Retrieval-Augmented-Generation-

cp .env.example .env
# Edit .env and set at minimum:
#   OPENAI_API_KEY=sk-...
#   JWT_SECRET_KEY=<random-256-bit-string>
```

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

The API will be available at **http://localhost:8000**.
Interactive docs: **http://localhost:8000/docs**

### 4. Ingest sample documents

```bash
# Get an admin token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/token \
  -H "Content-Type: application/json" \
  -d '{"user_id": "admin", "roles": ["admin", "all-employees"]}' \
  | jq -r .access_token)

# Ingest the /data directory
curl -s -X POST "http://localhost:8000/api/v1/ingest/directory?directory=/app/data" \
  -H "Authorization: Bearer $TOKEN" | jq
```

### 5. Chat

```bash
# Get a user token
USER_TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/token \
  -H "Content-Type: application/json" \
  -d '{"user_id": "alice", "roles": ["all-employees", "engineering"]}' \
  | jq -r .access_token)

# Ask a question
curl -s -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the parental leave policy?"}' | jq
```

### 6. Local development (without Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Download spaCy model for Presidio
python -m spacy download en_core_web_lg

# Run tests
pytest tests/ -v

# Start the API
uvicorn app.main:app --reload --port 8000
```

---

## Configuration

All configuration is via environment variables (see `.env.example`).

### Switch to Pinecone (one line)

```bash
VECTOR_DB=pinecone \
PINECONE_API_KEY=pcsk_... \
PINECONE_INDEX_NAME=healthtech-rag \
docker-compose up
```

### Switch to Claude

```bash
LLM_PROVIDER=anthropic \
ANTHROPIC_API_KEY=sk-ant-... \
docker-compose up
```

### Key variables

| Variable | Default | Description |
|---------|---------|-------------|
| `OPENAI_API_KEY` | (required) | OpenAI API key |
| `VECTOR_DB` | `chroma` | `chroma` or `pinecone` |
| `LLM_PROVIDER` | `openai` | `openai` or `anthropic` |
| `JWT_SECRET_KEY` | (required) | Signing secret for JWTs |
| `RETRIEVAL_TOP_K` | `20` | Candidates before reranking |
| `RERANK_TOP_N` | `6` | Final chunks sent to LLM |
| `ENABLE_PII_REDACTION` | `true` | Presidio PII redaction |
| `CONFIDENCE_THRESHOLD` | `0.35` | Below this → "I don't know" |

---

## API Reference

### POST `/api/v1/token` – Issue JWT (dev/testing)

```json
{
  "user_id": "alice",
  "roles": ["all-employees", "hr-team"]
}
```

### POST `/api/v1/chat` – RAG chat

**Headers:** `Authorization: Bearer <token>`

```json
{
  "query": "What is the 401k match policy?",
  "conversation_history": [],
  "query_rewrite_strategy": "hyde"
}
```

**Response:**

```json
{
  "answer": "HealthTech matches 100% of the first 4% of salary... [Source: benefits_overview.md]",
  "sources": [{"doc_id": "...", "filename": "benefits_overview.md", "score": 0.92}],
  "confidence": 0.87,
  "latency_ms": 1240,
  "guardrail_meta": {"citations_present": true, "hallucinated": false}
}
```

### POST `/api/v1/ingest/file` – Upload document

Requires `admin` role. Accepts `multipart/form-data` with:
- `file`: PDF, TXT, or Markdown
- `access_tags`: comma-separated role tags (e.g., `hr-team,admin`)
- `pii_flags`: comma-separated flags (e.g., `PHI,PII`)

### POST `/api/v1/ingest/directory` – Batch ingest (admin)

### GET `/health` – Health check

---

## Document Ingestion

Documents in `/data` use front-matter conventions to declare access control:

```markdown
**Access Tags:** hr-team          ← restricts to hr-team role
**PII Flags:** PHI,PII            ← tags for audit/guardrails
```

### Access Control (Row-Level Security)

| Document | Access Tags | Roles that can see it |
|---------|------------|----------------------|
| `company_handbook.md` | `all-employees` | Everyone |
| `benefits_overview.md` | `all-employees` | Everyone |
| `hr_salary_guidelines.md` | `hr-team` | HR team only |
| `medical_data_policy.md` | `compliance-team,engineering-leads,admin` | Compliance/leads |
| `it_security_policy.md` | `all-employees` | Everyone |
| `product_spec_v1.md` | `all-employees` | Everyone |
| `research_paper_rag.md` | `all-employees` | Everyone |

ACL filtering happens **before** vector retrieval via Chroma metadata filters,
ensuring unauthorized chunks never reach the LLM context window.

---

## Security & Compliance

### GDPR / HIPAA / CCPA Controls

| Control | Implementation |
|---------|---------------|
| PII redaction | Microsoft Presidio (input) |
| Row-level ACL | Chroma/Pinecone metadata filter pre-retrieval |
| Audit logging | Structured JSON to stdout + optional file |
| Secrets management | Environment variables / K8s secrets (KMS in prod) |
| TLS | Enforced at ingress (K8s) / reverse proxy |
| JWT auth | HS256 with configurable expiry |
| Prompt injection | Regex + LLM-based detection |

### Threat Model

- **Prompt injection:** Detected and blocked before processing.
- **Unauthorized PHI access:** ACL filter prevents retrieval of restricted chunks.
- **Hallucination:** LLM-as-judge + citation enforcement + confidence threshold.
- **Credential exposure:** No secrets in code; `.env` in `.gitignore`.

---

## Evaluation

### Running the offline evaluator

```bash
# Start the API first, then:
python -m eval.evaluator \
  --api-url http://localhost:8000 \
  --token $USER_TOKEN \
  --roles all-employees \
  --output eval_results.json
```

### Metrics (Blueprint §10)

| Metric | Target | Description |
|--------|--------|-------------|
| Recall@10 | ≥ 0.85 | Correct chunk in top-10 |
| MRR | ≥ 0.75 | Mean Reciprocal Rank |
| Answer F1 | ≥ 0.75 | Token F1 vs. reference answer |
| Hallucination Rate | ≤ 2% | LLM-judged unsupported claims |
| p95 Latency | < 1.8s | End-to-end |

### Golden set

`eval/golden_set.json` contains 30 QA pairs across 6 domains:
- HR policies (time off, benefits, onboarding)
- Product specs (ClinicalAI v1/v2)
- Security policies
- Compliance / PHI handling
- Engineering guidelines
- Adversarial / out-of-scope queries

---

## Production Deployment

### Kubernetes

```bash
kubectl create namespace healthtech
kubectl apply -f k8s/configmap.yaml  # Update secrets before applying!
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Scaling notes (Blueprint §17)

- **RBAC:** Extend `UserContext.roles` with fine-grained permissions; map to Chroma ACL tags.
- **Caching:** Plug Redis into `retrieve_and_rerank()` with a 5-min TTL for popular queries.
- **Synthetic queries:** Use `eval/evaluator.py` with generated QA pairs for continuous eval.
- **Dashboard:** Expose Prometheus metrics at `/metrics`; build Grafana SLO dashboard.
- **Horizontal scaling:** Chroma → Pinecone serverless removes vector DB as scaling bottleneck.

---

## Blueprint Compliance

| # | Blueprint Point | Status |
|---|----------------|--------|
| 1 | Use-case & requirements | ✅ Healthcare-tech enterprise, p95 < 1.8s, JWT auth |
| 2 | Architecture choice (RAG) | ✅ Standard RAG pipeline |
| 3 | Vector DB (Chroma + Pinecone) | ✅ One-line switch via `VECTOR_DB` |
| 4 | Embedding models | ✅ text-embedding-3-large + fine-tune stub |
| 5 | Chunking & preprocessing | ✅ Semantic, 200-400 tokens, 30-token overlap, pdfplumber |
| 6 | Index design | ✅ `{id, chunk_text, embedding, metadata}` + cosine similarity |
| 7 | Retrieval & reranking | ✅ bge-reranker-large + HyDE + multi-query |
| 8 | Generation layer | ✅ GPT-4o-mini default, Claude fallback, citation prompt |
| 9 | Guardrails & safety | ✅ Presidio PII, injection detection, LLM-judge, ACL pre-filter |
| 10 | Evaluation | ✅ 30-item golden set, Recall@K, MRR, F1, hallucination rate |
| 11 | MLOps / data ops | ✅ Webhook ingestion, batch ingestion, LangSmith tracing |
| 12 | Deployment stack | ✅ FastAPI + LangChain + Docker + docker-compose + K8s |
| 13 | Security & compliance | ✅ TLS at ingress, JWT, audit logs, row-level ACL |
| 14 | Cost control | ✅ Context capped at 6 chunks, batch embedding, model flag |
| 15 | Minimal flow | ✅ Implemented in `app/api/chat.py` |
| 16 | Sprint checklist | ✅ All items satisfied |
| 17 | Scaling & hardening | ✅ Placeholders in code + documented above |
| 18 | Beyond classic RAG | ✅ LangGraph stub below |

---

## Future: Agentic Extension

When to move beyond classic RAG (Blueprint §18):

> Move to agentic RAG when:
> - Queries require **multi-step reasoning** (e.g., compare two policies, calculate entitlements).
> - The system needs to **call external APIs** (HR system, ticketing, calendar).
> - **Dynamic tool selection** is needed based on query intent.
> - Latency budget allows > 3s (agents are slower due to multiple LLM calls).

```python
# ============================================================
# FUTURE EXTENSION: Agentic RAG with LangGraph
# Uncomment and install: pip install langgraph
# ============================================================

# from langgraph.graph import StateGraph, END
# from langchain_core.messages import HumanMessage
# from typing import TypedDict, Annotated
# import operator
#
# class AgentState(TypedDict):
#     messages: Annotated[list, operator.add]
#     retrieved_chunks: list
#     final_answer: str
#
# def retrieve_node(state: AgentState) -> AgentState:
#     """Node: retrieve relevant chunks."""
#     query = state["messages"][-1].content
#     chunks = retrieve_and_rerank(query, user_roles=["all-employees"])
#     return {"retrieved_chunks": chunks}
#
# def generate_node(state: AgentState) -> AgentState:
#     """Node: generate answer from chunks."""
#     # ... LLM call with retrieved context
#     return {"final_answer": "..."}
#
# def should_retrieve_more(state: AgentState) -> str:
#     """Conditional edge: check if we need more retrieval."""
#     if not state["retrieved_chunks"]:
#         return "retrieve"
#     return END
#
# # Build the graph
# workflow = StateGraph(AgentState)
# workflow.add_node("retrieve", retrieve_node)
# workflow.add_node("generate", generate_node)
# workflow.set_entry_point("retrieve")
# workflow.add_edge("retrieve", "generate")
# workflow.add_conditional_edges("generate", should_retrieve_more)
# agent = workflow.compile()
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

*Built with ❤️ by HealthTech Engineering. Questions? Open an issue or contact the AI Platform team.*