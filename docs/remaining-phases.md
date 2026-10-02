# TADS M11–M18 Completion Contract

The remaining milestones are implemented as explicit, testable contracts before external runtime deployment. The repository now also hardens the M9/M10 persistence boundary with append-only historical records and deferred equality checks between portable evidence snapshots and normalized lineage. This prevents documentation from claiming production capabilities that require infrastructure or verified external-provider APIs.

## M11 — Feedback & Learning
Outcome records are append-only inputs. Precision, recall and confidence calibration are deterministic evaluation primitives. Historical scoring inputs are never mutated by future outcomes. Temporal evaluation rejects future-label leakage and supports as-of eligibility. Historical scoring inputs are never mutated by future outcomes.

## M12 — Console
The console must consume the existing evidence lineage and expose account timeline, why-now, score decomposition, recommendation rationale and audit history. The domain contract is intentionally UI-neutral; presentation belongs to the future application surface.

## M13 — Productionization
Runtime health/readiness is explicit. Database, migrations, source ingestion and integrations are independent readiness signals. Deployment must add object storage, telemetry, backups, migrations/rollback and resource quotas before production activation.

## M14 — Security & Privacy
The security policy contract requires trusted tenant context, hostile-content treatment, untrusted model output, restricted egress, secret redaction, personal-data minimization and auditability. These complement the existing PostgreSQL/RLS and controlled-ingestion controls.

## M15 — Reliability & Scale
Retries are bounded and deterministic. Idempotency remains a domain requirement for source ingestion and derived persistence. Production workers must add queue semantics, dead-letter handling, backpressure, circuit breakers and load-tested capacity.

## M16 — Governance & Compliance
Governance records bind a control owner, review state, timestamp and evidence. Retention policy prevents personal-data retention from exceeding the broader evidence window.

## M17 — E2E + Adversarial Validation
The canonical E2E chain is represented as a closed set of stages. A validation run is incomplete if any stage is absent.

## M18 — Enterprise GA
The enterprise gate is fail-closed: CI, security, tenant isolation, documentation, E2E validation, rollback testing, governance, provider verification, production deployment, backup/restore, observability, adversarial validation, load testing, disaster recovery, privacy review and supply-chain verification must all have explicit evidence before readiness can become READY.

These contracts are deliberately not a substitute for deployment infrastructure, verified ReconOS/FadeReach APIs, legal review, load testing or operational evidence. Those remain environment-dependent release gates.
