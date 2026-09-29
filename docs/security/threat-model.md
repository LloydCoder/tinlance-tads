# TADS Threat Model

## Security posture

TADS assumes external content is hostile and treats model output as untrusted unless a separate policy layer authorizes it.

The security lifecycle follows defense-in-depth and can be mapped to NIST AI RMF's Govern, Map, Measure and Manage functions. OWASP guidance is used for application and GenAI-specific threat classes.

## Assets

- tenant and account intelligence
- source snapshots/evidence
- provider credentials
- personal data
- entity-resolution decisions
- scoring/taxonomy policies
- agent trajectories and research artifacts
- integration credentials
- audit records

## Trust boundaries

1. Internet/provider → fetcher
2. fetcher → parser/normalizer
3. normalized data → TADS domain
4. TADS → PostgreSQL/object storage
5. TADS → Agent Platform
6. TADS → ReconOS
7. TADS → FadeReach

## Threats and required controls

### SSRF and egress abuse

Threats include internal IP targeting, DNS rebinding, unsafe redirects, alternate URL schemes and metadata-service access.

Controls:

- HTTPS-only
- explicit source host allowlists
- strict URL parser
- reject URL userinfo
- standard-port policy
- resolve and validate public addresses
- redirect rejection/revalidation
- response timeout and byte budgets
- network-layer egress restrictions
- no arbitrary URL fetches from model output

OWASP specifically recommends allowlists where feasible and warns that redirect handling can bypass validation; it also recommends network-layer controls. https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html

### Parser/resource exhaustion

Controls: response limits, compression policy, parser depth limits, page budgets, concurrency limits, worker timeouts, cancellation and quarantine.

### Prompt injection

Retrieved content is data, never instructions. Agents receive content through typed evidence channels; tool authorization is independent of page text.

### Data poisoning

Keep source provenance, timestamps, source reliability, contradictions and hashes. Never collapse contradictory evidence into certainty.

### False entity merge

Use deterministic candidate generation, confidence thresholds, ambiguity states and evidence-backed review. Never silently merge on a weak name match.

### Tenant escape

All tenant records are scoped and RLS-protected. Application roles must be least privileged and must not expose arbitrary SQL. PostgreSQL notes that table owners/superusers/BYPASSRLS roles bypass RLS and that referential-integrity checks bypass row security; this is why RLS is one layer, not the entire trust boundary. https://www.postgresql.org/docs/18/ddl-rowsecurity.html and https://www.postgresql.org/docs/17/role-attributes.html

### Secret leakage

Credentials never enter logs, evidence, prompts, fixtures or client responses. Secrets remain in the deployment/platform secret boundary.

### Privacy overcollection

Prefer organization-level intelligence. Person-level data requires explicit purpose, minimization, lawful basis, retention and deletion controls.

### Supply-chain risk

Pin and audit dependencies; later productionization adds SBOM, provenance/signing and vulnerability gates.

### Excessive agency

Agent actions require explicit tool scopes, budgets, timeouts, approvals and policy. Model output never becomes authorization.

## Current implemented controls

M1: PostgreSQL migrations/checksums, tenant RLS, cross-tenant parent checks, immutable evidence and integration tests.

M2: controlled fetch policy, public-address validation, HTTPS/host restrictions, redirect rejection, content-type/size/time budgets, source adapters and ingestion provenance.

M3: ambiguity-preserving deterministic entity resolution and tenant-scoped resolution candidates.

M4: typed signal taxonomy/detection, quality dimensions and tenant-scoped signal persistence.

## Security gates before GA

- trusted tenant-context mechanism
- network-layer egress enforcement
- comprehensive SSRF regression corpus
- parser fuzz/resource exhaustion tests
- prompt-injection fixtures
- secret-redaction tests
- dependency/SBOM/provenance controls
- privacy/retention/deletion automation
- authorization and audit verification
- full adversarial E2E tests


## M9–M18 assurance additions

### Integration boundary
ReconOS and FadeReach are treated as separate trust boundaries. TADS sends only typed, purpose-limited contracts and requires evidence on returned enrichment and opportunity handoffs. No provider response is treated as authority without provenance.

### Agentic risks
TADS agent specifications prohibit outreach and require explicit evidence. Agent Platform remains responsible for runtime tool authorization, sandboxing, approvals and generic audit. This separation addresses excessive agency and tool-misuse risks.

### Supply-chain controls
CI actions are pinned to immutable commit SHAs. GitHub recommends full-length SHA pinning for third-party actions to reduce the risk of mutable-tag compromise. Dependencies and workflow changes remain reviewable artifacts.

### Readiness gates
M18 is fail-closed. CI success alone is insufficient: tenant isolation, security controls, documentation reconciliation, E2E validation, rollback evidence and governance review are independently required.

The security posture is aligned to OWASP Top 10:2025, whose current categories include broken access control, security misconfiguration, software supply-chain failures, injection, insecure design, authentication failures, software/data integrity, logging/alerting failures and exceptional-condition handling.
