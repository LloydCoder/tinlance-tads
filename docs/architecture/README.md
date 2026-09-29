# TADS Architecture

## 1. Mission

TADS converts permitted observations into auditable intelligence:

`source → observation → canonical event → entity → account → signal → temporal context → account state → opportunity hypothesis → recommendation`

The architecture is deliberately **evidence-first**. The system must be able to answer:

- what was observed?
- from which source?
- when was it published, observed and detected?
- how was it normalized?
- which canonical entity was selected?
- what alternatives were considered?
- which evidence supports the claim?
- which policy/version produced the derived result?
- what remains unknown or contradictory?

## 2. Ownership boundaries

### TADS

TADS owns domain intelligence: ingestion contracts, observations, canonical events, identity resolution, signal taxonomy/detection, temporal correlation, account state, ICP, opportunity reasoning, recommendations and feedback.

### Agent Platform

Agent Platform owns generic execution controls: agent runtime/orchestration, model routing, tool authorization, sandboxing, approvals, generic evidence/provenance/audit, memory/retrieval, budgets, eventing and platform telemetry.

TADS must integrate through a versioned capability contract. It must never silently assume an Agent Platform API that has not been tested.

### ReconOS

ReconOS performs deep enrichment/OSINT. TADS requests enrichment and consumes evidence; it does not duplicate ReconOS.

### FadeReach

FadeReach handles research-to-engagement execution. TADS may publish a versioned opportunity handoff but never sends outreach.

## 3. Planes

```
SOURCE PLANE
registry → policy → fetcher → validation → snapshot → observation

IDENTITY PLANE
observation → normalization → candidate generation → resolution decision → organization/account

SIGNAL PLANE
canonical event → taxonomy → detection → quality → evidence → lifecycle

CONTEXT PLANE
signal timeline → temporal features → correlation → account state

OPPORTUNITY PLANE
ICP → hypothesis → score → explanation → recommendation

INTEGRATION PLANE
ReconOS enrichment → human review → FadeReach handoff → outcomes

CONTROL PLANE
tenant → authorization → provenance → audit → privacy → observability → budgets
```

## 4. Processing contract

1. **Fetch** only permitted source material.
2. **Validate** URL, scheme, host, DNS result, redirect behavior, size, content type, encoding and timeout.
3. **Snapshot** immutable source material metadata and content hash.
4. **Observe** create a normalized observation with source provenance.
5. **Normalize** source-specific fields without making identity or intent claims.
6. **Resolve** generate candidates and preserve ambiguity.
7. **Canonicalize** represent the real-world event once while retaining supporting observations.
8. **Classify** produce typed signals only from observed/canonical facts.
9. **Correlate** combine signals across time only under explicit deterministic rules.
10. **Score** produce versioned, explainable components.
11. **Hypothesize** separate facts from interpretation and unknowns.
12. **Recommend** produce a bounded action proposal.
13. **Record outcome** without rewriting historical knowledge.

## 5. Trust boundaries

External content is hostile input. Fetching, parsing and model execution are separate trust boundaries.

```
Internet/provider
      │ untrusted
      ▼
controlled fetcher
      │ validated snapshot
      ▼
parser / normalizer
      │ candidate facts
      ▼
TADS domain kernel
      │ authenticated tenant context
      ▼
PostgreSQL / object storage
      │ versioned adapters
      ├── Agent Platform
      ├── ReconOS
      └── FadeReach
```

OWASP recommends allowlisting where feasible, redirect controls and network-layer egress restrictions for SSRF defense; TADS therefore treats application URL validation as necessary but not sufficient. citeturn0search0

## 6. Data architecture

PostgreSQL is the system of record. Relational relationship tables provide graph behavior initially. A graph database requires measured evidence that PostgreSQL is insufficient.

Large source content belongs in immutable object storage; PostgreSQL stores metadata, hashes, locators and lineage.

## 7. Determinism and reproducibility

Every derived artifact carries a policy/taxonomy/version identifier and its input references. Deterministic stages must be replayable from frozen fixtures.

ML/LLM layers, when eventually introduced, are advisory unless a separate authorization contract explicitly grants an action. They may summarize evidence; they may not manufacture evidence.

## 8. Multi-tenancy

All tenant-scoped tables carry a tenant key and RLS policy. Application connections must use a trusted tenant context; client/model free text cannot directly set tenant identity.

PostgreSQL explicitly documents that RLS can be bypassed by table owners, superusers and BYPASSRLS roles, and that foreign-key/referential-integrity checks bypass row security. citeturn0search2

Therefore the architecture uses:

- least-privileged application role
- no tenant-facing raw SQL
- tenant context established by trusted application infrastructure
- cross-tenant parent-reference checks
- regression tests for reads, writes and foreign-key references
- explicit enterprise hardening before GA

## 9. Deployment

Initial form: modular monolith with API and worker boundaries. Add queues/brokers only when throughput, isolation or recovery requirements justify them.

Recommended components:

- Python 3.12+
- PostgreSQL 17+
- strict async HTTP client
- object storage
- OpenTelemetry-compatible telemetry
- containerized API/worker
- managed secret store

## 10. Architectural non-goals

No universal crawler, LinkedIn scraper, generic lead database, CRM, outreach engine, premature graph database, or ML-only intent predictor.
