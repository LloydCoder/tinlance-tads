# TADS Production Runbook

## M13 production gate

TADS must not be declared production-ready merely because CI is green. The deployment environment must
provide all of the following:

1. PostgreSQL with managed backups and tested restore procedures.
2. Immutable object storage for large source snapshots.
3. A secret manager; credentials must not be stored in repository configuration or evidence.
4. OpenTelemetry-compatible metrics, traces and logs with secret/PII redaction.
5. API and worker runtime boundaries with bounded concurrency.
6. Migration execution with checksum verification and an approved rollback procedure.
7. Rate limits, quotas and resource budgets.
8. Network-layer egress policy for ingestion and integrations.
9. Health/readiness probes that fail closed when database, migrations, ingestion or integrations are unhealthy.
10. Alerting and incident-response ownership.

## Required environment configuration

- DATABASE_URL
- OBJECT_STORAGE_ENDPOINT
- OTEL_EXPORTER_OTLP_ENDPOINT

Production values must use managed infrastructure and HTTPS where applicable. Never place credentials in
these variables' committed examples or documentation.

## Release evidence

A production release record must include:

- deployed artifact identifier;
- migration checksum set;
- configuration/schema compatibility result;
- backup timestamp and restore-test result;
- health/readiness result;
- telemetry verification;
- rollback test result;
- security and privacy gate results;
- operator and incident owner.

## Fail-closed rule

If a required production dependency is absent, incompatible or unverifiable, readiness remains blocked.
A local development environment is not evidence of production readiness.
