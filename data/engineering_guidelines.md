# HealthTech Inc. – Engineering Guidelines & Best Practices

**Version:** 2025-Q1 | **Owner:** VP Engineering
**Access Tags:** all-employees

---

## 1. Engineering Principles

1. **Reliability over cleverness.** Write boring, predictable code. Clever code is a liability.
2. **Observability first.** Every service must emit structured logs, metrics, and traces before launch.
3. **Security by design.** Threat model early; never retrofit security.
4. **Ship incrementally.** Small PRs (<400 lines) merged frequently beat large quarterly drops.
5. **Automate toil.** If you do it manually twice, automate it on the third occurrence.

---

## 2. Technology Standards

### 2.1 Languages & Runtimes

| Use Case | Preferred | Acceptable |
|---------|---------|-----------|
| Backend APIs | Python 3.11+ (FastAPI) | Go 1.22+ |
| Data pipelines | Python 3.11+ | Spark (PySpark) |
| Frontend | TypeScript / React 18 | – |
| Infrastructure | Terraform + HCL | CDK (Python) |
| Scripts / automation | Python | Bash (simple tasks only) |

### 2.2 Database Choices

| Type | Preferred | Notes |
|------|---------|-------|
| Relational | PostgreSQL 16 | Use RLS for multi-tenant |
| Vector | Chroma (dev) / Pinecone (prod) | Cosine similarity |
| Cache | Redis 7.x | Redis Cluster for prod |
| Object store | AWS S3 | Versioning + encryption mandatory |
| Message queue | AWS SQS / SNS | FIFO queues for ordered processing |

### 2.3 Frameworks

| Purpose | Standard |
|---------|---------|
| HTTP API | FastAPI + Pydantic v2 |
| LLM orchestration | LangChain (latest stable) |
| ORM | SQLAlchemy 2.x (async) |
| Task queue | Celery + Redis broker |
| Testing | pytest + pytest-asyncio |
| Linting | ruff + mypy (strict) |

---

## 3. Code Review Standards

### 3.1 Pull Request Requirements

- PR must have a clear description: what, why, how.
- All PRs require at least **1 approval** from a team member + **1 approval** from a senior engineer
  for production code paths.
- PR must be linked to a Jira ticket.
- All automated checks (lint, tests, security scan) must pass before merge.
- PR size limit: **400 lines of logic code** (excluding generated/auto-formatted files).
  Larger PRs require justification in the PR description.

### 3.2 Review Checklist

Reviewers should verify:
- [ ] Correctness: does the code do what the description says?
- [ ] Tests: are new behaviors covered? Are edge cases addressed?
- [ ] Security: no secrets in code, no new attack surface, proper input validation
- [ ] Performance: no N+1 queries, no blocking I/O in async paths
- [ ] Observability: structured logs, metrics, traces for new code paths
- [ ] Documentation: updated if public APIs change

---

## 4. Testing Standards

| Test Type | Coverage Target | Tool |
|---------|----------------|------|
| Unit tests | 85% line coverage | pytest |
| Integration tests | All API endpoints | pytest + httpx |
| Contract tests | All external service integrations | pytest |
| Load tests | p95 < SLA for all endpoints | Locust |
| Security tests | SAST + DAST in CI | Bandit + OWASP ZAP |

Tests must run in < 5 minutes (unit) and < 15 minutes (integration) in CI.

---

## 5. Deployment & Branching

### 5.1 Git Workflow

- **main:** Always deployable. Protected; requires PR + passing CI.
- **feature/\*:** Feature branches. Merged to main via PR.
- **hotfix/\*:** Emergency fixes. Require expedited review + post-incident review.
- No force-pushes to main or release branches.

### 5.2 Environments

| Environment | Purpose | Deploy Trigger |
|------------|--------|---------------|
| dev | Local development | docker-compose |
| staging | Integration testing | PR merge to main |
| production | Customer traffic | Manual approval after staging validation |

### 5.3 Release Process

1. Code merged to main → staging deployed automatically.
2. Staging smoke tests pass → create release tag (semver).
3. Release tag triggers production deploy with canary (10% → 50% → 100% over 2 hours).
4. If p99 error rate > 1% during canary, automatic rollback.

---

## 6. Incident Management

### 6.1 Severity Definitions

| SEV | Definition | Response Time |
|-----|-----------|--------------|
| SEV-1 | Total service outage or patient safety issue | 5 min |
| SEV-2 | Major feature unavailable; >25% of users affected | 15 min |
| SEV-3 | Degraded performance or minor feature broken | 30 min |
| SEV-4 | Non-impacting bug; cosmetic issue | Next sprint |

### 6.2 On-Call

- All IC4+ engineers participate in on-call rotation.
- PagerDuty escalation: L1 (oncall) → L2 (team lead) → L3 (VP Eng) after 10 min.
- Post-incident review (PIR) required for all SEV-1 and SEV-2 incidents.

---

## 7. API Design Standards

- RESTful resource naming: plural nouns, lowercase, hyphenated (e.g., `/v1/patient-records`).
- Use HTTP status codes correctly (200, 201, 400, 401, 403, 404, 409, 422, 500).
- All request/response bodies must use JSON with Pydantic models.
- API versions in URL path (e.g., `/v1/`, `/v2/`).
- Pagination: cursor-based for large collections; max 100 items per page.
- Rate limiting: 100 req/min per API key (default); higher limits via negotiation.

---

## 8. Observability Requirements

Every production service must have:
- **Structured JSON logs** with: timestamp, level, service, trace_id, request_id, user_id.
- **Prometheus metrics** exported on `/metrics`: request count, latency histograms, error rate.
- **Distributed traces** via OpenTelemetry → Datadog APM.
- **Health check** endpoint at `/health` (200 OK if healthy).
- **SLO dashboards** in Datadog: availability (99.9%), p95 latency, error rate.

---

*Questions? Ask in #engineering-guild on Slack.*
