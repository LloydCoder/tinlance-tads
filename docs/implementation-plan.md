# TADS Implementation Plan

## Completion rule

A milestone is complete only when implementation, tests, security controls, documentation, CI and post-merge main validation agree. A contract is not represented as a deployed capability.

## M0–M8 — Intelligence foundation

**Status: COMPLETE.** The repository contains the architecture/governance foundation, evidence-first PostgreSQL kernel, controlled ingestion, deterministic entity resolution, signal engine, temporal correlation, account intelligence, ICP/opportunity scoring and governed agent specifications.

## M9 — ReconOS integration

**Status: ADAPTER-COMPLETE; EXTERNAL-VERIFICATION GATE REMAINS.**

Delivered:
- purpose-limited `EnrichmentRequest`
- evidence-required `EnrichmentResult`
- provider/version attribution
- tenant-scoped enrichment persistence
- normalized evidence-link table
- cross-tenant parent checks
- no assumed external ReconOS API

Remaining environment gate: verify the actual ReconOS service against `docs/architecture/provider-capability-contracts.md`, including authenticated capability, scopes, schema/version, rate limits, provenance and failure semantics.

## M10 — FadeReach integration

**Status: ADAPTER-COMPLETE; EXTERNAL-VERIFICATION GATE REMAINS.**

Delivered:
- bounded `OpportunityHandoff`
- evidence-required handoff
- tenant-scoped immutable persistence boundary
- normalized evidence-link table
- explicit no-outreach invariant
- provider-neutral port

Remaining environment gate: verify the actual FadeReach service against `docs/architecture/provider-capability-contracts.md`, including authenticated capability, scopes, schema/version, idempotency, expiry, rate limits and failure semantics.

## M11 — Feedback & Learning

**Status: EVALUATION-COMPLETE; OPERATIONAL EVALUATION GATE REMAINS.**

Delivered:
- append-only tenant-scoped evaluation outcome persistence
- idempotent outcome ingestion
- precision/recall primitive
- confidence calibration primitive
- temporal prediction/label ordering invariant
- as-of evaluation eligibility to prevent future-label leakage
- PostgreSQL RLS and append-only regression coverage

Production gate: representative outcome corpus, monitored calibration, drift/error monitoring and production evaluation telemetry.

## M12 — Console

**Status: PROJECTION-COMPLETE; UI/DEPLOYMENT GATE REMAINS.**

The versioned console projection now requires evidence, explicit score decomposition, unknowns and optional audit references and exposes a bounded public serialization surface. UI implementation remains intentionally separate from the intelligence kernel.

Production gate: authenticated UI, tenant-aware authorization, audit-history integration, accessibility, browser security controls and production deployment verification.

## M13 — Productionization

**Status: CONTRACT-HARDENED; OPERATIONAL GATE REMAINS.**

Delivered:
- explicit runtime readiness model
- fail-closed production configuration
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

**Status: CONTRACT-HARDENED; OPERATIONAL GATE REMAINS.**

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

**Status: CONTRACT-HARDENED; OPERATIONAL GATE REMAINS.**

Delivered bounded exponential retry policy, bounded capacity and idempotency policies.

Production gate:
- idempotency keys at every retryable boundary
- queue/DLQ semantics
- backpressure
- circuit breakers
- load/capacity tests
- RPO/RTO and disaster-recovery exercises

## M16 — Governance & Compliance

**Status: CONTRACT-HARDENED; OPERATIONAL GATE REMAINS.**

Delivered governance record, review cadence and retention contracts.

Production gate:
- control owners and review cadence
- vendor/source governance
- access reviews
- incident/change management
- data residency decisions
- documented legal/privacy assessments

## M17 — End-to-end adversarial validation

**Status: CONTRACT-HARDENED; EXECUTABLE ADVERSARIAL GATE REMAINS.**

The canonical chain is a closed validation set:

`source → observation → event → entity → account → signal → temporal → account state → opportunity → ReconOS → FadeReach → outcome → feedback`

Production gate: executable E2E fixtures, poisoning/prompt-injection/tenant-escape tests, failure injection and reproducible audit artifacts.

## M18 — Enterprise GA

**Status: FAIL-CLOSED ENTERPRISE GATE IMPLEMENTED; GA EVIDENCE REMAINS.**

The enterprise gate now additionally requires provider verification, production deployment, backup/restore, observability, adversarial validation, load testing, disaster recovery, privacy review and supply-chain verification.

**M18 is not declared deployed GA until those environment-dependent gates have real evidence.**

## Persistence hardening after M9/M10

Migration 0010 hardens the integration boundary and historical intelligence model. It makes historical artifacts append-only for the application role, enforces exact equality between portable JSON evidence snapshots and normalized evidence-link tables with deferred PostgreSQL constraint triggers, and keeps lifecycle tables explicitly mutable.

This hardening is part of the contract layer; production still requires adversarial validation of role ownership, deployment privileges and operational backup/restore behavior.

## Cross-cutting controls

Security, privacy, provenance, data quality, observability, testing, evaluation, cost controls, documentation and governance remain active at every milestone.
