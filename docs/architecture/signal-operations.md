# Signal Operations & Drift

X3 makes signal behavior observable over time without mutating historical evidence.

## Lifecycle

Signals may be detected, strengthened, weakened, corroborated, contradicted, marked stale, expired or reactivated. Every lifecycle event requires evidence and a timezone-aware timestamp.

Lifecycle history is append-only and chronological.

## Drift

The X3 primitive tracks false-positive rate, false-negative rate, source-reliability delta and taxonomy-change rate independently. Drift is detected when any monitored metric reaches the configured threshold.

These metrics are evaluation inputs, not opportunity scores.

## Boundary

X3 does not rewrite signal history and does not execute retraining. Production monitoring, representative labels and remediation workflows remain part of the M11/M18 operational evidence program.
