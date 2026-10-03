# TADS Remaining Phases

The M0–M18 implementation sequence is complete/hardened. The project now has a controlled X1–X8 extension sequence plus the existing M18 operational evidence gates.

## X1 — Source Control Plane
**Implementation-complete.** Source registration, lifecycle, health and fail-closed activation are implemented and tested. Durable PostgreSQL persistence and production source onboarding remain operational gates.

## X2 — Data Quality & Evidence Trust
Add freshness, completeness, consistency, source reliability, identity confidence, temporal validity, corroboration and contradiction as independent quality dimensions.

## X3 — Signal Operations & Drift
Add signal lifecycle, source reliability, false-positive/false-negative monitoring and drift controls.

## X4 — Change Intelligence
Add deterministic account-state transitions and material-change detection over the existing temporal kernel.

## X5 — Intelligence Graph
Add a PostgreSQL-backed graph abstraction for evidence and intelligence relationships. A dedicated graph database remains deferred until measured need exists.

## X6 — Buying Windows
Add evidence-backed buying-window lifecycle semantics without converting them into claims of purchase intent.

## X7 — Intelligence Subscriptions & Alerts
Add account, segment, signal and opportunity watches with materiality filtering. TADS does not become an outreach engine.

## X8 — Evaluation & Experimentation
Expand M11 into an operational evaluation platform for detection, ranking, temporal leakage, calibration and drift.

## Enterprise GA evidence

After X8, M18 remains fail-closed until the following are evidenced: provider contracts verified; production deployment; backup/restore; observability; adversarial validation; load testing; disaster recovery; privacy review; and supply-chain verification.

No documentation may represent an evidence gate as complete merely because a code contract exists.
