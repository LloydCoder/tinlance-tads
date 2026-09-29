# TADS Implementation Plan

## Completion rule

A milestone is complete only when implementation, tests, security controls, documentation, CI and post-merge main validation agree. A contract is not represented as a deployed capability.

## M0–M8 — Intelligence foundation

**Status: COMPLETE.** The repository contains the architecture/governance foundation, evidence-first PostgreSQL kernel, controlled ingestion, deterministic entity resolution, signal engine, temporal correlation, account intelligence, ICP/opportunity scoring and governed agent specifications.

## M9 — ReconOS integration

**Status: CONTRACT-COMPLETE.**

Delivered:
- purpose-limited `EnrichmentRequest`
- evidence-required `EnrichmentResult`
- provider/version attribution
- tenant-scoped enrichment persistence
- normalized evidence-link table
- cross-tenant parent checks
- no assumed external ReconOS API

Remaining environment gate: implement and verify the actual ReconOS adapter only after its authenticated capability contract, scopes, rate limits, provenance and failure semantics are documented.

## M10 — FadeReach integration

**Status: CONTRACT-COMPLETE.**

Delivered:
- bounded `OpportunityHandoff`
- evidence-required handoff
- tenant-scoped immutable persistence boundary
- normalized evidence-link table
- explicit no-outreach invariant
- provider-neutral port

Remaining environment gate: verify the actual FadeReach capability contract before connecting a provider.

## M11 — Feedback & Learning

**Status: CONTRACT-COMPLETE.**

Delivered:
- append-only outcome model
- precision/recall primitive
- confidence calibration primitive
- explicit separation of decision-time state from later outcome data

Production gate: outcome ingestion, calibration corpus, temporal leakage tests and monitored evaluation.

## M12 — Console

**Status: CONTRACT-COMPLETE.**

The domain contract is ready for a separate console surface exposing evidence, timeline, why-now, score decomposition, recommendation rationale and audit history. UI implementation is intentionally separate from the intelligence kernel.

## M13 — Productionization

**Status: CONTRACT-COMPLETE.**

Delivered:
- explicit runtime readiness model
- independent database, migration, ingestion and integration health dimensions

Production gate:
- API/worker runtime
- object storage
- telemetry
- deployment manifests
- secret manager
- backup/restore
- migration rollback
- quotas/rate limits
- resource budgets

## M14 — Security & Privacy

**Status: CONTRACT-COMPLETE.**

Delivered fail-closed security policy covering trusted tenant context, hostile external content, untrusted model output, restricted egress, secret redaction, personal-data minimization and auditability.

Production gate:
- network enforcement
- authorization verification
- privacy/legal review
- deletion/retention automation
- SSRF/resource-exhaustion corpus
- prompt-injection fixtures
- supply-chain/SBOM/provenance controls

## M15 — Reliability & Scale

**Status: CONTRACT-COMPLETE.**

Delivered bounded exponential retry policy.

Production gate:
- idempotency keys at every retryable boundary
- queue/DLQ semantics
- backpressure
- circuit breakers
- load/capacity tests
- RPO/RTO and disaster-recovery exercises

## M16 — Governance & Compliance

**Status: CONTRACT-COMPLETE.**

Delivered governance record and retention contracts.

Production gate:
- control owners and review cadence
- vendor/source governance
- access reviews
- incident/change management
- data residency decisions
- documented legal/privacy assessments

## M17 — End-to-end adversarial validation

**Status: CONTRACT-COMPLETE.**

The canonical chain is a closed validation set:

`source → observation → event → entity → account → signal → temporal → account state → opportunity → ReconOS → FadeReach → outcome → feedback`

Production gate: executable E2E fixtures, poisoning/prompt-injection/tenant-escape tests, failure injection and reproducible audit artifacts.

## M18 — Enterprise GA

**Status: CONTRACT-COMPLETE.**

The enterprise gate is fail-closed and requires CI, security, tenant isolation, documentation, E2E validation, rollback testing and governance review.

**M18 is not declared deployed GA until those environment-dependent gates have real evidence.**

## Persistence hardening after M9/M10

Migration 0010 hardens the integration boundary and historical intelligence model. It makes historical artifacts append-only for the application role, enforces exact equality between portable JSON evidence snapshots and normalized evidence-link tables with deferred PostgreSQL constraint triggers, and keeps lifecycle tables explicitly mutable.

This hardening is part of the contract layer; production still requires adversarial validation of role ownership, deployment privileges and operational backup/restore behavior.

## Cross-cutting controls

Security, privacy, provenance, data quality, observability, testing, evaluation, cost controls, documentation and governance remain active at every milestone.
