# Source Control Plane

## Purpose

TADS separates source governance from source fetching.

- tads_sources decides whether a registered source is allowed to participate in ingestion.
- tads_ingest performs the controlled fetch and normalization.
- tads_contracts.SourceContract remains the stable policy contract.
- tads_db will own durable registry persistence when operational deployment requires it.

The source control plane is intentionally fail-closed.

## Lifecycle

```text
REGISTERED → ACTIVE → SUSPENDED
      │          │
      └──────────┴────→ RETIRED
```

Activation requires both an enabled source contract and explicit legal/provider review.

Suspended and retired sources cannot be ingested. Retirement disables the source contract and is terminal.

## Health

Health is independent from authorization: UNKNOWN, HEALTHY, DEGRADED and FAILED.

A health result never grants permission to ingest. Health timestamps must be timezone-aware and connector versions are retained with the registry record.

## Security boundary

The registry does not trust fetched content, URLs supplied by external content, model output or provider responses. Those remain untrusted data at the ingestion boundary.

The registry does not implement fetching, crawling, OSINT, authorization bypass, rate-limit bypass or provider-specific network behavior.

## Operational persistence

The current X1 implementation is an in-memory deterministic control-plane primitive. Durable multi-tenant persistence is deliberately deferred to the database implementation when production deployment evidence is available. This avoids creating a second source-of-truth outside PostgreSQL.

## X1 completion rule

X1 is implementation-complete when lifecycle transitions are deterministic, activation is fail-closed, retirement disables the contract, health timestamps are validated, duplicate registration is rejected, tests/lint/typing/CI are green, and architecture documentation agrees.

Production source onboarding remains an operational M13/M14 governance gate.
