# TADS Persistence / Migration Baseline — M0

M0 establishes persistence rules for M1. It does not claim that a production database exists.

## System of record

PostgreSQL is the planned system of record. The first implementation should use a modular relational schema, with JSONB only for genuinely source-shaped or extensible data.

## Migration invariants

1. Every schema change is an ordered, immutable migration.
2. Migrations are forward-only in shared environments.
3. Destructive changes require an explicit expand/migrate/contract plan.
4. Application code remains compatible with the deployed schema during rollout.
5. Tenant-scoped tables require an explicit tenant key and server-side tenant context.
6. Evidence references are immutable after creation except for narrowly defined metadata corrections.
7. Canonical identity merges require provenance and an auditable decision record.
8. No migration may silently delete historical evidence.
9. Migration tests run against real PostgreSQL once M1 schema work begins.
10. Backup/restore validation is a production gate.

## M1 starting set

Tenant, Account, Organization, Domain, Source, SourceSnapshot, Observation, CanonicalEvent, Evidence, Relationship, Signal, SignalCluster, AccountState, Opportunity, OpportunityHypothesis, OpportunityScore, Recommendation, Action, Feedback, Outcome.

## Deferred from M0

Production schema implementation, ORM choice, database provisioning, RLS implementation, search index, graph database, and queue/broker are M1/M13 work. M0 freezes the invariants without pretending that placeholders are a database.
