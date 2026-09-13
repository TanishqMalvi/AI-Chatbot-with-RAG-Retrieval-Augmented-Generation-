
# Engineering Guidelines

**Version:** 4.1 | **Owner:** VP of Engineering

## Code Review
- All changes require at least one approval from a code owner.
- Reviews should be completed within 24 business hours.
- Focus on correctness, security, performance, and maintainability.
- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.

## Pull Requests
- PRs should be < 400 lines when possible; split large changes.
- Include tests for new behavior; update docs for API changes.
- CI must pass: lint, type-check, unit tests, security scan.
- Link PR to ticket; summarize change, risk, and rollout plan.

## Testing
- Unit test coverage target: 80% line coverage.
- Integration tests for API endpoints and data pipelines.
- E2E tests for critical user journeys via Cypress.
- Use property-based testing for complex algorithms where feasible.

## Observability
- Instrument services with structured logging (`structlog`) and OpenTelemetry spans.
- Emit metrics for latency, error rate, saturation.
- Dashboards must include at least: p50, p95, p99 latency; request rate; error rate.
- Alerting thresholds documented in runbooks.

## Incident Response
- Severity 1: page on-call engineer, open war room within 15 min.
- Severity 2: notify team lead, resolution within 4 hours.
- Severity 3: ticket, resolution within 2 business days.
- Post-incident review required for Severity 1 and 2 within 48 hours.

## API Design
- RESTful endpoints with consistent naming: `/api/v1/<resource>`
- Request/response schemas defined with Pydantic v2.
- Pagination: cursor-based for large collections; limit default 20, max 100.
- Versioning: include version in URL path; deprecate old versions with ≥ 90 days notice.
