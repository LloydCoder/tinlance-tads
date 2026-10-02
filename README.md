# Tinlance TADS

**Target / Account / Demand Signal Intelligence**

[![CI](https://github.com/LloydCoder/tinlance-tads/actions/workflows/ci.yml/badge.svg)](https://github.com/LloydCoder/tinlance-tads/actions/workflows/ci.yml)

TADS is Tinlance's **evidence-first account-intelligence substrate**. It turns permitted source observations into traceable signals, temporal context, account state, bounded opportunity hypotheses and explainable recommendations.

> **Who matters? What changed? Why does it matter? Why now? What evidence supports the conclusion? What remains unknown?**

TADS is designed to produce **reconstructable intelligence**, not opaque lead scores.

## What TADS is — and is not

TADS is:

- an account-intelligence and demand-signal kernel;
- evidence- and provenance-first;
- conservative about identity resolution;
- deterministic at its core;
- explicit about uncertainty and unknowns;
- multi-tenant with database-enforced isolation;
- provider-neutral at integration boundaries;
- designed to feed Tinlance's wider agent and product stack.

TADS is **not**:

- a CRM;
- a generic lead database;
- a universal crawler;
- a LinkedIn scraper;
- an intent oracle;
- an outreach engine;
- a replacement for ReconOS deep enrichment;
- a replacement for Agent Platform execution controls;
- a purchase-probability predictor.

## Core intelligence chain

```text
permitted source
    │
    ▼
source policy → fetch → snapshot → observation
    │
    ▼
canonical event
    │
    ▼
entity resolution ──► organization / tenant account
    │
    ▼
signal detection → evidence / quality / lifecycle
    │
    ▼
temporal correlation
    │
    ▼
account state
    │
    ▼
ICP + opportunity hypothesis
    │
    ▼
score + rationale + unknowns
    │
    ▼
bounded recommendation
    │
    ├──────────────► ReconOS enrichment
    │
    └──────────────► FadeReach intelligence handoff
                              │
                              ▼
                           outcomes
                              │
                              ▼
                           feedback
```

The canonical evidence chain is:

```
source
→ snapshot
→ observation
→ canonical event
→ entity/account
→ signal
→ temporal context
→ account state
→ opportunity
→ integration handoff
→ outcome
→ feedback
```

Every material derived artifact must remain reconstructable to its supporting evidence and the policy/taxonomy/version that produced it.

## Non-negotiable invariants

1. **Observation ≠ signal.**
2. **Signal ≠ intent.**
3. **Intent ≠ opportunity.**
4. **Opportunity ≠ customer.**
5. **Evidence ≠ interpretation.**
6. **Unknown beats fabrication.**
7. **Ambiguity beats a false entity merge.**
8. **Scores must be reproducible from their declared components.**
9. **Material intelligence must retain evidence lineage.**
10. **Tenant identity comes from trusted server-side context.**
11. **External content and model output are untrusted data, never authorization.**
12. **TADS never executes outreach.**

## Architecture and ownership

### TADS owns

- source policy and source adapters;
- immutable source snapshots and observations;
- canonical events;
- conservative entity resolution;
- signal taxonomy and deterministic detection;
- temporal correlation;
- account intelligence;
- ICP and opportunity hypotheses;
- scoring and recommendation contracts;
- outcome/evaluation primitives;
- TADS-specific feedback and research workflows.

### Tinlance Agent Platform owns

- generic agent runtime/orchestration;
- model routing;
- tool authorization;
- sandboxing;
- approvals;
- generic audit/provenance;
- memory/retrieval;
- platform budgets, eventing and telemetry.

TADS consumes these capabilities through explicit, versioned contracts. It does not duplicate them.

### ReconOS owns

Deep enrichment / OSINT. TADS requests purpose-limited enrichment and consumes evidence-backed results; it does not embed a second OSINT engine.

### FadeReach owns

Engagement execution. TADS can publish a versioned, evidence-backed opportunity handoff; it **does not send email, create outreach sequences, automate social activity or manage follow-ups**.

## Milestone status

| Milestone | Current state | What exists |
|---|---|---|
| M0 | ✅ Complete | Architecture, governance, boundaries and typed domain contracts |
| M1 | ✅ Complete | PostgreSQL evidence-first kernel, RLS, tenant isolation and immutable evidence |
| M2 | ✅ Complete | Controlled ingestion, source policy and provenance |
| M3 | ✅ Complete | Conservative entity resolution with ambiguity preservation |
| M4 | ✅ Complete | Deterministic signal taxonomy/detection and evidence lineage |
| M5 | ✅ Complete | Temporal/correlation feature kernel with evidence propagation |
| M6 | ✅ Complete | Explainable, evidence-preserving account-state derivation |
| M7 | ✅ Complete | Deterministic ICP/opportunity scoring and recommendations |
| M8 | ✅ Complete | Governed agent specifications; execution remains Agent Platform-owned |
| M9 | 🚧 Adapter-complete | Authenticated fail-closed ReconOS adapter; external capability verification remains |
| M10 | 🚧 Adapter-complete | Authenticated fail-closed FadeReach handoff adapter; external capability verification remains |
| M11 | 🚧 Evaluation-complete | Immutable outcome ingestion, temporal leakage controls and evaluation primitives; operational corpus/monitoring remains |
| M12 | 🚧 Projection-complete | Versioned evidence-first console projection; authenticated UI/deployment remains |
| M13 | 🚧 Contract-complete | Runtime readiness contract |
| M14 | 🚧 Contract-complete | Fail-closed security/privacy contract |
| M15 | 🚧 Contract-complete | Bounded deterministic retry contract |
| M16 | 🚧 Contract-complete | Governance and retention contracts |
| M17 | 🚧 Contract-complete | Closed canonical E2E validation contract |
| M18 | 🚧 Contract-complete | Fail-closed enterprise GA gate |

**Contract-complete is intentionally not called production-deployed.** Real ReconOS/FadeReach adapters, production infrastructure, network enforcement, backup/restore evidence, load testing, disaster recovery, legal/privacy review, operational telemetry and other environment-dependent controls remain release gates.

## Repository map

```text
src/
├── tads_contracts/       # Stable domain, provenance, scoring, source and taxonomy contracts
├── tads_ingest/          # Safe fetching, source adapters and ingestion orchestration
├── tads_resolution/      # Entity normalization and ambiguity-preserving resolution
├── tads_signals/         # Evidence-first deterministic signal detection
├── tads_temporal/        # Time-window and correlation features
├── tads_accounts/        # Explainable account-state derivation
├── tads_opportunities/   # ICP and opportunity reasoning
├── tads_agents/          # Governed agent specifications; no runtime execution
├── tads_integrations/    # Canonical ReconOS/FadeReach contracts and ports
├── tads_assurance/       # M11–M18 security, reliability, governance and readiness contracts
├── tads_console/         # UI-neutral evidence-preserving console projection
├── tads_runtime/         # Runtime health/readiness contract
└── tads_db/              # PostgreSQL connection, repositories and migrations

database/                 # Human-facing migration documentation
docs/                     # Architecture, security, source policy and milestone contracts
tests/                    # Unit, architecture and PostgreSQL integration tests
.github/workflows/        # CI quality and integration gates
```

## Evidence-first design

TADS keeps several concepts deliberately separate.

### Observation

A source-level fact captured from a permitted snapshot. It does not imply identity, intent or opportunity.

### Canonical event

A normalized real-world change supported by one or more observations. Multiple observations may support the same event.

### Signal

A deterministic classification derived from observed/canonical facts. Signals carry evidence and quality dimensions such as strength, freshness and reliability.

### Temporal context

TADS distinguishes publication, effective, observation, detection, first-seen, last-seen and expiry times. A disappearance is absence evidence, not proof of the opposite event.

### Account state

A versioned materialized view of evidence and context, including signal strength/diversity, momentum, negative evidence and data confidence.

### Opportunity hypothesis

A bounded interpretation that keeps **observed facts, interpretation, potential problem, capability fit, confidence, unknowns and evidence** separate.

### Recommendation

A bounded next-step proposal such as `MONITOR`, `RESEARCH`, `ENRICH`, `REQUEST_HUMAN_REVIEW` or `CREATE_OPPORTUNITY`. It is not a claim that an account will buy.

## Integration boundaries

M9/M10 use one canonical integration model under `tads_integrations`.

- `EnrichmentRequest` — purpose-limited ReconOS request.
- `EnrichmentResult` — provider/version-attributed result requiring evidence.
- `OpportunityHandoff` — evidence-backed intelligence handoff toward FadeReach.
- `ReconOSPort` / `FadeReachPort` — provider-neutral adapter boundaries.

The older M0 import names in `tads_contracts.integration` are compatibility aliases to these canonical models; they are not a second contract implementation.

## Multi-tenancy and database security

PostgreSQL is the system of record.

The database uses:

- tenant-scoped relations;
- Row-Level Security;
- trusted transaction-local tenant context;
- cross-tenant parent-reference triggers;
- least-privileged `tads_app` role;
- immutable evidence;
- append-only historical intelligence boundaries;
- migration checksums and an advisory transaction lock;
- normalized evidence-link tables;
- deferred consistency checks between portable evidence snapshots and authoritative lineage.

RLS is defense in depth, not the only tenant boundary. PostgreSQL documents that table owners and roles with `BYPASSRLS` can bypass row security, and referential-integrity checks have special behavior. The application therefore combines RLS with least privilege and explicit tenant-parent validation.

## Source policy

Public reachability is **not** authorization.

TADS permits documented, licensed, customer-authorized or otherwise lawful access and prohibits:

- bypassing authentication or access controls;
- bypassing CAPTCHAs or rate limits;
- LinkedIn scraping or automated activity without explicit authorization;
- leaked/stolen/unlawfully disclosed datasets;
- unnecessary sensitive personal-data collection.

Initial structured adapters cover documented Greenhouse public Job Board access and authenticated Lever access. Source activation remains subject to terms, purpose, geography, retention, privacy and rate-limit review.

## Security posture

The ingestion boundary treats URLs and retrieved content as hostile input. Application controls include:

- HTTPS-only URLs;
- explicit source host allowlists;
- rejection of URL userinfo and non-standard ports;
- public-address validation;
- redirect rejection;
- response byte/time/content-type budgets;
- secret-safe handling;
- tenant isolation;
- evidence provenance;
- fail-closed readiness.

Production network-layer egress enforcement remains mandatory because application-layer URL validation alone cannot eliminate DNS/network race conditions.

The security program is aligned with current OWASP application-security guidance, including access control, security misconfiguration, software supply-chain integrity, injection, insecure design, data/software integrity, logging/alerting and exceptional-condition handling.

## Quick start

### Requirements

- Python **3.12+**
- PostgreSQL **17+**
- Git

### Install

```bash
git clone https://github.com/LloydCoder/tinlance-tads.git
cd tinlance-tads

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

### Run migrations

```bash
export DATABASE_URL='postgresql://postgres:postgres@127.0.0.1:5432/tads_test'
python -m tads_db.migrate
```

### Run quality gates

```python -m ruff format --check src tests
python -m ruff check src tests
python -m mypy
python -m pytest
```

PostgreSQL integration tests run automatically when `DATABASE_URL` is present. CI provisions PostgreSQL 17 as an ephemeral service.

## CI quality bar

Every change must satisfy:

1. formatting;
2. lint;
3. strict mypy;
4. unit/contract tests;
5. PostgreSQL integration tests;
6. architecture-boundary tests;
7. documentation contract tests;
8. migration integrity checks.

GitHub Actions uses least-privilege repository permissions, immutable commit-SHA-pinned actions and disabled checkout credential persistence.

**CI green is necessary, not sufficient for enterprise GA.** M13–M18 contain explicit environment-dependent release gates.

## Documentation map

| Document | Purpose |
|---|---|
| `docs/architecture/README.md` | System architecture and ownership |
| `docs/architecture/data-model.md` | Canonical semantic data model |
| `docs/architecture/integration-boundaries.md` | Agent Platform / ReconOS / FadeReach boundaries |
| `docs/architecture/provider-capability-contracts.md` | External provider schemas, authentication and verification gates |
| `docs/architecture/migration-baseline.md` | Persistence and migration invariants |
| `docs/data-source-policy.md` | Source authorization and collection policy |
| `docs/security/threat-model.md` | Threats, trust boundaries and required controls |
| `docs/security/ci-hardening.md` | CI supply-chain and permission controls |
| `docs/implementation-plan.md` | Authoritative M0–M18 milestone plan |
| `docs/remaining-phases.md` | M11–M18 completion and production gates |

The implementation plan is authoritative for milestone status; the README is the developer-facing summary.

## Development principles

### Prefer deterministic primitives

Core intelligence should be replayable from frozen inputs. LLMs may summarize or assist research but cannot manufacture facts or grant authorization.

### Preserve uncertainty

Unknown, ambiguous and contradictory states are first-class. TADS should lose precision before it invents certainty.

### Keep boundaries explicit

Integration contracts do not silently become product implementations. Agent Platform, ReconOS and FadeReach remain separately owned systems.

### Make security structural

Tenant isolation, evidence lineage, source policy, append-only history and fail-closed readiness belong in code and database controls, not only in documentation.

### Avoid premature infrastructure

The modular-monolith shape remains the default until measured workload, isolation, recovery or integration requirements justify queues, brokers, additional services or a graph database.

## Project maturity

The current repository is a **production-oriented intelligence kernel with M0–M8 implemented and M9–M18 contract-complete**.

That distinction is deliberate. TADS does not claim external-provider integration, production deployment, legal approval, disaster recovery or enterprise GA merely because a type or test exists.

The next implementation layer is therefore environment-specific productionization: connect verified provider capabilities, deploy the runtime, enforce network and identity controls, execute adversarial E2E tests, validate recovery/scale, and collect the evidence required by the M18 gate.

## License

Proprietary — see [LICENSE](LICENSE).

## Tinlance

TADS is part of the Tinlance engineering stack. Ownership and integration boundaries described in this repository are intentional architectural constraints.
