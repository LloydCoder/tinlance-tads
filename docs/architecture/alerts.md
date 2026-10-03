# Intelligence Subscriptions & Alerts

X7 adds watches for accounts, segments, signals, opportunities and buying windows.

## Materiality

Alerts are emitted only when a deterministic materiality threshold is met and evidence is present. Dedupe keys prevent repeated delivery of the same material event.

## Boundary

TADS produces an evidence-backed alert event. It does not send email, social messages, sequences or follow-ups. Channel delivery belongs to the surrounding application/engagement stack.

Tenant identity is part of the watch and must come from trusted server-side context in production.
