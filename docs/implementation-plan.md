# TADS Implementation Plan

## Delivery rule

A milestone is **complete only when implementation, tests, security gates, documentation, CI and post-merge main validation all agree**. Architecture alone is not completion.

## M0 — Architecture & Governance

**Status: COMPLETE**

Delivered: product/domain boundaries, Agent Platform/ReconOS/FadeReach ownership, evidence invariant, temporal semantics, source governance, threat model, typed contracts, migration/persistence invariants, architecture tests, proprietary license and CI.

## M1 — Intelligence Kernel

**Status: COMPLETE**

Delivered: PostgreSQL 17 integration, checksummed ordered migrations, tenant-scoped persistence, RLS, tenant context, cross-tenant parent-reference guards, immutable evidence, source snapshots, observations, canonical events, evidence, signals, repositories and integration tests.

Exit chain: source → snapshot → observation → canonical event → account → evidence → signal.

## M2 — Source Ingestion

**Status: COMPLETE**

Delivered:

- source registry/fetch boundary
- HTTPS and host policy
- public-address validation
- redirect rejection
- request timeout/byte/content-type budgets
- normalized observation transport
- Greenhouse public Job Board adapter
- authenticated Lever postings adapter
- source snapshot/observation persistence
- ingestion-run/fetch-attempt persistence
- content hashing and provenance
- SSRF-adjacent regression coverage

Explicitly excluded: universal crawler, anonymous Lever access, LinkedIn scraping, model-driven fetching.

## M3 — Entity Resolution

**Status: COMPLETE**

Delivered:

- conservative name/domain normalization
- exact-domain and alias evidence
- deterministic candidate scoring
- MATCHED / PROBABLE / AMBIGUOUS / UNRESOLVED states
- no-silent-merge invariant
- tenant-scoped aliases and resolution candidates
- evidence-reference slots
- regression tests for exact, ambiguous and unknown cases

Remaining hardening that must be completed before M3 is considered enterprise-grade: parent/subsidiary/acquisition relationship semantics, golden resolution corpus, precision/recall metrics and adversarial false-merge tests.

## M4 — Signal Engine

**Status: IN PROGRESS**

Current implementation:

- versioned signal taxonomy
- deterministic source-aware detection
- hiring/security signal classification
- strength/freshness/reliability quality dimensions
- composite quality
- signal lifecycle state
- tenant-scoped signal persistence
- deterministic deduplication constraint
- regression tests

M4 exit requirements:

1. canonical-event input contract rather than provider-specific-only detection
2. observation/evidence linkage for every signal
3. explicit negative/contradictory signal handling
4. taxonomy registry and versioning
5. persistence repository and idempotent writes
6. signal quality tests and boundary cases
7. signal provenance and replay fixtures
8. M4 documentation reconciled with code
9. green CI and merged PR

## M5 — Temporal & Correlation

**Status: IN PROGRESS**

Current implementation:
- deterministic event-window filtering
- frequency/density features
- signal diversity
- source independence
- temporal momentum
- contradiction ratio
- versioned correlation rules
- tenant-scoped PostgreSQL correlation persistence
- replayable unit fixtures

M5 exit requirements still include explicit decay policy, sequence-pattern rules, persisted signal membership/lineage, contradiction evidence semantics, repository idempotency where required, and adversarial temporal fixtures.

## M6 — Account Intelligence

- account timeline
- materialized account state
- ICP context
- technical/business context
- negative evidence
- historical versions
- explainable drivers

## M7 — ICP + Opportunity Engine

- configurable ICP profiles
- deterministic opportunity score
- confidence/calibration
- evidence-backed hypotheses
- negative factors and unknowns
- recommendation policy
- human-review thresholds

## M8 — Agent Intelligence

Only introduce agents where deterministic code is insufficient. Agent Platform remains the execution/control substrate. TADS owns domain tools, evidence contracts and evaluations.

## M9 — ReconOS

Versioned authenticated enrichment adapter. Do not duplicate OSINT capability.

## M10 — FadeReach

Versioned opportunity handoff. No outreach execution in TADS.

## M11 — Feedback & Learning

Capture outcomes without leaking future outcomes into historical scoring inputs. Add calibration, precision/recall and decision-quality evaluation.

## M12 — Console

Account intelligence, timeline, why-now, evidence, hypothesis, score decomposition, recommendations and audit history.

## M13 — Productionization

API/worker runtime, object storage, health/readiness, observability, deployment, migrations, rollback, backup/restore, quotas, rate limits and cost controls.

## M14 — Security & Privacy

Trusted tenant boundary, encryption, secrets, audit, privacy workflows, lawful-source enforcement, network egress, SSRF, poisoning, prompt-injection, supply-chain and resource-limit controls.

## M15 — Reliability & Scale

Retries, idempotency, replay, dead-letter handling, checkpointing, backpressure, circuit breakers, graceful degradation, capacity/load tests, RPO/RTO and disaster recovery.

## M16 — Governance & Compliance

Security/privacy policies, vendor governance, data residency, retention, access reviews, change management, incidents, continuity, risk and audit evidence.

## M17 — E2E + Adversarial Validation

Prove and attack:

`source → observation → event → entity → account → signal → temporal context → account state → ICP → opportunity → ReconOS → FadeReach → outcome → feedback`

Completion requires runtime evidence, adversarial fixtures and reproducible CI.

## M18 — Enterprise GA

Continuous source-health, data-quality, security, model/signal evaluation, entity-resolution accuracy, opportunity calibration, SLO/cost monitoring, incident response, DR tests, access reviews, regression and red-team assurance.

## Cross-cutting controls

Security, privacy, provenance, observability, data quality, testing, evaluation, cost controls, documentation and governance are active at every milestone.
