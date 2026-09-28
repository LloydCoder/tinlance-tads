# TADS database migrations

Migrations are ordered, immutable SQL files.

M1 establishes the PostgreSQL evidence-first kernel. Every tenant-scoped relation carries tenant_id, and row-level security uses the server-side transaction setting app.tenant_id.

The application sets tenant context inside a transaction with SELECT set_config('app.tenant_id', '<tenant-uuid>', true). The true flag makes the setting transaction-local.

Evidence rows are immutable by database trigger. Historical observations and snapshots are append-only.

Run migrations through python -m tads_db.migrate. The runner records applied filenames in schema_migrations and rejects unknown history.