# TADS Implementation Plan

## Completion rule

A milestone is complete only when implementation, tests, security controls, documentation, CI and post-merge main validation agree. A contract is not represented as a deployed capability.

## M0–M18

**Status: IMPLEMENTED/HARDENED.** The original intelligence and enterprise-assurance sequence is implemented. M9–M18 retain environment-dependent operational gates; M18 remains fail-closed until those gates have real evidence.

## X1 — Source Control Plane

**Status: IMPLEMENTATION-COMPLETE; OPERATIONAL PERSISTENCE/ONBOARDING GATE REMAINS.**

Delivered:
- fail-closed source registration;
- registered/active/suspended/retired lifecycle;
- activation requires enabled contract plus legal/provider review;
- terminal retirement disables the source contract;
- independent health state and timezone-aware timestamps;
- connector-version attribution;
- deterministic ingestion eligibility;
- duplicate-registration protection.

Operational gate:
- durable PostgreSQL registry persistence;
- tenant/vendor/source ownership;
- production onboarding approvals;
- terms/rate-limit enforcement.

## X2 — Data Quality & Evidence Trust

**Status: IMPLEMENTATION-COMPLETE; PRODUCTION CALIBRATION GATE REMAINS.**

Delivered independent dimensions for freshness, completeness, consistency, source reliability, identity confidence, temporal validity, corroboration and contradiction, plus deterministic eligibility thresholds. Quality is not an intelligence/opportunity score.

Operational gate: representative production corpus, source-specific calibration and monitored quality thresholds.

## X3 — Signal Operations & Drift

**Status: IMPLEMENTATION-COMPLETE; PRODUCTION MONITORING GATE REMAINS.**

Delivered append-only signal lifecycle events, chronological/evidence invariants and deterministic drift metrics covering false positives, false negatives, source reliability and taxonomy change.

Operational gate: representative labels, production monitoring and remediation workflow.

## X4 — Change Intelligence

**Status: IMPLEMENTATION-COMPLETE; CORPUS-DEPENDENT HIGHER-ORDER INTERPRETATION GATE REMAINS.**

Delivered evidence-backed account-state snapshots, emergence, material-change and disappearance semantics. Acceleration, deceleration and reversal are deliberately not fabricated without sufficient temporal corpus evidence.

Operational gate: representative longitudinal corpus and validated higher-order transition logic.

## X5 — Intelligence Graph

**Status: IMPLEMENTATION-COMPLETE; SCALE/PERFORMANCE GATE REMAINS.**

Delivered a PostgreSQL-compatible evidence/intelligence graph abstraction with evidence-backed edges and deterministic traversal.

Operational gate: measure traversal depth, latency, volume and storage before considering a dedicated graph database.

## X6 — Buying Windows

**Status: IMPLEMENTATION-COMPLETE; PRODUCTION VALIDATION GATE REMAINS.**

Delivered bounded EMERGING/ACTIVE/COOLING/DORMANT/INVALIDATED lifecycle semantics with explicit expiry, triggers and evidence. Buying windows cannot claim purchase intent.

Operational gate: validate lifecycle quality against representative outcomes without collapsing the distinction between evidence and intent.

## X7 — Intelligence Subscriptions & Alerts

**Status: IMPLEMENTATION-COMPLETE; APPLICATION DELIVERY GATE REMAINS.**

Delivered tenant-scoped watch contracts, materiality filtering and deterministic alert deduplication.

Operational gate: authenticated application surface, tenant authorization and downstream channel delivery.

## X8 — Evaluation & Experimentation

**Status: IMPLEMENTATION-COMPLETE; OPERATIONAL EVALUATION GATE REMAINS.**

Delivered deterministic detection, ranking, calibration and drift metrics plus reproducible evaluation-run controls for corpus, as-of time, code version, taxonomy version and leakage status.

Operational gate: representative outcome corpus, monitored calibration, drift/error telemetry and production evaluation cadence.

## Enterprise GA gates

After X8, the existing M18 operational evidence gates remain authoritative:

1. provider contracts verified;
2. production deployed;
3. backup/restore verified;
4. observability verified;
5. adversarial validation complete;
6. load testing complete;
7. disaster recovery tested;
8. privacy review complete;
9. supply chain verified.

These are evidence gates, not additional architecture modules.

## Cross-cutting controls

Security, privacy, provenance, data quality, observability, testing, evaluation, cost controls, documentation and governance remain active at every milestone.
