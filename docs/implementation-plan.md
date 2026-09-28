# TADS Implementation Plan

## M0 — Architecture Foundation

Status: **COMPLETE**

M0 is complete when the repository contains explicit, reviewable contracts for the TADS domain boundary and the controls required before production intelligence code.

Completed:
- repository and product boundary
- Agent Platform ownership boundary
- ReconOS enrichment boundary
- FadeReach intelligence-handoff boundary
- canonical intelligence processing contract
- canonical data model and evidence invariant
- temporal semantics
- source governance and permitted-access policy
- security threat model and AI/security framework alignment
- persistence and migration invariants
- typed source, taxonomy, provenance, observation, event, signal, scoring, and integration contracts
- deterministic score recomputation contract
- architecture boundary tests
- evidence-first domain tests
- typed-package marker
- proprietary license declaration
- CI with formatting, linting, type checking, and contract tests

M0 deliberately does not claim implementation of the production database, ingestion runtime, entity resolver, signal engine, opportunity engine, agents, ReconOS adapter, FadeReach adapter, console, or production deployment.

## M1 — Evidence-First Intelligence Kernel

Build the first real runtime domain layer:
- PostgreSQL schema and immutable migrations
- tenant/account/entity repositories
- source and source-snapshot persistence
- observation and canonical-event persistence
- evidence/provenance persistence
- signal persistence
- relationship persistence
- deterministic API schemas
- tenant-isolation tests
- migration tests against PostgreSQL
- one reproducible evidence chain from source to signal

M1 exit condition: a real permitted source can be represented as source → snapshot → observation → event → account/entity → signal → evidence with reconstructable lineage.

## M2 — Source Ingestion

Start with controlled public structured sources and first-party data. Greenhouse Job Board and Lever public postings remain candidate initial hiring-signal adapters, subject to revalidation of provider contracts and terms before release. Public web fetching comes only after the hardened fetch boundary is implemented.

## M3 — Entity Resolution

- normalization
- domain/legal-name/alias matching
- parent/subsidiary/acquisition relationships
- confidence and ambiguity states
- golden resolution dataset
- false-merge regression tests

## M4 — Signal Detection

- versioned taxonomy
- event canonicalization
- deduplication
- signal-quality dimensions
- temporal decay
- signal lifecycle

## M5 — Temporal and Correlation Intelligence

- event-time semantics
- recency and decay
- frequency and density
- sequence detection
- diversity and independence
- momentum
- contradiction handling
- reproducible correlation rules

## M6 — Account Intelligence

- account timeline
- materialized account state
- ICP context
- technical/business context
- negative evidence
- historical state versions
- explainable drivers

## M7 — ICP, Opportunity, and Recommendation

- configurable ICP profiles
- deterministic opportunity score
- confidence and calibration hooks
- evidence-backed hypotheses
- negative factors and unknowns
- recommendation policy
- human-review thresholds

## M8 — Agent Intelligence

Agents are introduced only where deterministic code is insufficient. Agent Platform remains the execution and control substrate. TADS owns domain tools, agent specifications, evidence requirements, and evaluations.

## M9 — ReconOS

Request enrichment and consume returned evidence through a versioned, authenticated adapter. Do not duplicate OSINT capability.

## M10 — FadeReach

Publish a versioned opportunity handoff. TADS does not execute outreach, sequences, social automation, or follow-up.

## M11 — Feedback and Outcomes

Capture recommendation → action → response → meeting → proposal → won/lost → value/retention outcomes. Prevent outcome leakage into historical intelligence and evaluate score calibration.

## M12 — Console

Account intelligence, signal timeline, why-now explanation, evidence, hypotheses, score decomposition, recommendations, and audit history.

## M13 — Productionization

API/worker runtime, PostgreSQL, object storage, queue/eventing only where justified, observability, health/readiness, migrations, deployment automation, rollback, backup/restore, rate limits, quotas, and cost controls.

## M14 — Security, Privacy, and Trust

Authentication, authorization, tenant isolation, encryption, secrets, audit, PII minimization, retention/deletion, lawful source controls, egress policy, SSRF defenses, prompt-injection defenses, poisoning defenses, supply-chain controls, output validation, agent permissions, and resource limits.

## M15 — Reliability and Scale

Retries, idempotency, dead-letter handling, checkpointing, replay, backpressure, circuit breakers, timeouts, graceful degradation, backup/restore, disaster recovery, RPO/RTO, capacity and load testing.

## M16 — Enterprise Governance

Security/privacy policies, vendor/subprocessor governance, data residency, retention, access reviews, change management, incident management, continuity, risk management, and audit evidence.

## M17 — Full-System E2E and Adversarial Validation

Prove and attack the full path:

source → observation → event → entity → account → signal → evidence → temporal correlation → account state → ICP → opportunity → ReconOS → FadeReach → outcome → feedback.

Completion requires runtime evidence, adversarial tests, and reproducible fixtures.

## M18 — Enterprise GA and Continuous Assurance

Continuous dependency/source health, data quality, security monitoring, model evaluation, signal precision, entity-resolution accuracy, opportunity calibration, cost/SLO monitoring, incident response, DR tests, access reviews, regression, and red-team assurance.

## Cross-cutting controls

Security, privacy, provenance, observability, data quality, testing, evaluation, cost controls, documentation, and governance start at M0 and evolve continuously. Milestone numbering is a delivery sequence, not permission to postpone those controls until the later hardening milestones.
