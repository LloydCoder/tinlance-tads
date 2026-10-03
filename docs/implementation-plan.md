# TADS Implementation Plan

## Completion rule

A milestone is complete only when implementation, tests, security controls, documentation, CI and post-merge main validation agree. A contract is not represented as a deployed capability.

## M0–M18

The original M0–M18 intelligence and enterprise-assurance sequence is implemented/hardened. M9–M18 retain environment-dependent operational gates; M18 remains fail-closed until those gates have real evidence.

## X1 — Source Control Plane

**Status: IMPLEMENTATION-COMPLETE; OPERATIONAL PERSISTENCE/ONBOARDING GATE REMAINS.**

Delivered:
- fail-closed source registration;
- lifecycle states: registered, active, suspended and retired;
- activation requires enabled contract plus legal/provider review;
- retirement disables the source contract and is terminal;
- independent source health state;
- timezone-aware health timestamps;
- connector-version attribution;
- deterministic ingestion-allowed decision;
- duplicate-registration protection;
- unit regression coverage.

Boundary:
- tads_sources governs source eligibility;
- tads_ingest fetches and normalizes;
- tads_contracts owns the stable source policy contract;
- tads_db remains the eventual durable source-registry owner.

Operational gate:
- persist the registry in PostgreSQL;
- enforce tenant/vendor/source ownership;
- connect source onboarding approvals;
- verify production rate-limit and terms controls.

## X2 — Data Quality & Evidence Trust

**Status: PLANNED.**

Add independent quality dimensions for freshness, completeness, consistency, source reliability, identity confidence, temporal validity, corroboration and contradiction. Quality must remain separate from intelligence/opportunity scores.

## X3 — Signal Operations & Drift

**Status: PLANNED.**

Add signal lifecycle, source-specific reliability, false-positive/false-negative monitoring, taxonomy drift and detection drift. Connect production outcomes to signal evaluation without mutating historical evidence.

## X4 — Change Intelligence

**Status: PLANNED.**

Add deterministic account-state transitions, emergence, acceleration, deceleration, reversal, disappearance and sustained-change semantics over the existing temporal and account layers.

## X5 — Intelligence Graph

**Status: PLANNED.**

Add a graph abstraction over PostgreSQL for evidence, events, entities, capabilities, signals and opportunities. Do not introduce a graph database until measured workload requires it.

## X6 — Buying Windows

**Status: PLANNED.**

Add bounded buying-window lifecycle semantics derived from evidence-backed combinations of account state, signals and changes. TADS must never represent a buying window as certainty of purchase intent.

## X7 — Intelligence Subscriptions & Alerts

**Status: PLANNED.**

Add account/segment/signal/opportunity watches and material-change events. Downstream delivery remains outside TADS's outreach boundary.

## X8 — Evaluation & Experimentation

**Status: PLANNED.**

Elevate M11 evaluation primitives into an operational evaluation platform covering detection, ranking, temporal leakage, calibration, drift and production monitoring.

## Enterprise GA gates

After the extension sequence, the existing M18 operational evidence gates remain authoritative: provider contracts verified; production deployed; backup/restore verified; observability verified; adversarial validation complete; load testing complete; disaster recovery tested; privacy review complete; supply chain verified.

These are evidence gates, not additional architecture modules.

## Cross-cutting controls

Security, privacy, provenance, data quality, observability, testing, evaluation, cost controls, documentation and governance remain active at every milestone.
