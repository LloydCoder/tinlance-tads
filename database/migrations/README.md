# TADS database migrations

Migrations are ordered, immutable SQL files. Executable migrations live in src/tads_db/migrations so packaged deployments receive the exact same migration set.

M1 establishes the PostgreSQL evidence-first kernel. Every tenant-scoped relation carries tenant_id, and row-level security uses the server-side transaction setting app.tenant_id.

The application sets tenant context inside a transaction with SELECT set_config('app.tenant_id', '<tenant-uuid>', true). The true flag makes the setting transaction-local.

Evidence rows are immutable by database trigger. Historical observations and snapshots are append-only.

Run migrations through python -m tads_db.migrate. The runner records applied filenames in schema_migrations and rejects unknown history.

## Integrity hardening

Migrations 0010 and 0011 extend the M9/M10 boundary with:

- append-only application-role enforcement for historical intelligence;
- exact deferred equality between JSON evidence snapshots and normalized evidence-link rows;
- tenant-scoped request/response identifiers for enrichment;
- tenant-scoped idempotency keys for FadeReach handoffs;
- explicit handoff expiry;
- lifecycle-only mutation privileges for ingestion-attempt state and signal-detection lifecycle records.

The normalized evidence-link tables are authoritative. Portable JSON evidence identifiers are retained only as a serialized contract snapshot and must reconcile exactly at transaction commit.
