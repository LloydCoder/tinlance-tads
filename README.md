# Tinlance TADS

**Target / Account / Demand Signal Intelligence**

TADS is Tinlance's evidence-first intelligence engine for answering five questions:

> **Who matters? What changed? Why does it matter? Why now? What should we do next?**

TADS does **not** equate a signal with buying intent. It turns permitted observations into traceable account intelligence, bounded opportunity hypotheses, and explainable recommendations.

## Product boundary

```
PERMITTED EXTERNAL / FIRST-PARTY SOURCES
                │
                ▼
M2  Source Registry → Fetch Policy → Fetcher → Snapshot → Observation
                │
                ▼
M3  Entity Resolution → Canonical Organization / Account
                │
                ▼
M4  Signal Detection → Typed Signal + Evidence + Quality
                │
                ▼
M5  Temporal / Correlation Intelligence
                │
                ▼
M6  Account Intelligence
                │
                ▼
M7  ICP + Opportunity + Recommendation
                │
       ┌────────┴─────────┐
       ▼                  ▼
    ReconOS            FadeReach
 enrichment          engagement handoff
       │                  │
       └────────┬─────────┘
                ▼
        Human decision / outcome
                │
                ▼
M11 Feedback → M12 Console → M13–M18 production, trust, scale and assurance
```

### TADS owns

- source registry and ingestion policy
- source-specific adapters and normalized observations
- canonical identity and entity-resolution decisions
- signal taxonomy, detection and lifecycle
- temporal correlation and signal stacking
- account state and intelligence timelines
- configurable ICP
- opportunity hypotheses and deterministic explainable scoring
- recommendations, feedback and outcome evaluation
- TADS-specific research workflows

### TADS does not own

- generic agent runtime, model routing, tool authorization, sandboxing or generic audit infrastructure — **Agent Platform**
- deep OSINT/enrichment — **ReconOS**
- outreach, campaigns, sequences or social automation — **FadeReach**
- CRM/contact-database behavior
- unauthorized platform scraping
- a universal web crawler
- unsupported claims of purchase intent

## Non-negotiable intelligence invariants

1. **Observation ≠ Signal**
2. **Signal ≠ Intent**
3. **Intent ≠ Opportunity**
4. **Opportunity ≠ Customer**
5. **Evidence ≠ Interpretation**
6. **Unknown beats fabrication**
7. **Ambiguity beats a false entity merge**
8. **Every material claim is reconstructable to evidence**
9. **Every tenant-scoped operation is server-side tenant controlled**
10. **External content is hostile data, never authority**

## Current implementation status

| Milestone | Status | What is actually implemented |
|---|---|---|
| M0 | ✅ Complete | Architecture, boundaries, governance, threat model, data contracts and repository gates |
| M1 | ✅ Complete | PostgreSQL kernel, migrations, RLS, tenant context, immutable evidence, repositories and integration tests |
| M2 | ✅ Complete | Controlled source ingestion boundary, Greenhouse public adapter, authenticated Lever adapter, snapshots/observations and SSRF-adjacent regression tests |
| M3 | ✅ Complete | Conservative identity normalization, domain/alias evidence, deterministic candidate scoring, ambiguity-preserving resolution and tenant-scoped resolution records |
| M4 | ✅ Complete | Deterministic signal taxonomy/detection, explicit evidence requirements, signal-quality dimensions, detection/evidence lineage, idempotent persistence and regression coverage |
| M5 | 🚧 In progress | Deterministic temporal/correlation feature kernel and tenant-scoped persistence |\n| M6–M18 | ⏳ Planned | Each milestone remains gated by executable implementation, tests, documentation and green CI; no future milestone is represented as shipped |

**The repository intentionally does not claim that a milestone is complete merely because its architecture has been designed.**

## Evidence chain

TADS maintains a reconstructable lineage:

`source → snapshot → observation → canonical event → entity/account → signal → evidence → correlation → account state → opportunity → recommendation`

Derived intelligence must preserve the inputs and policy/version used to create it. Re-running a deterministic policy against the same frozen inputs must produce the same result.

## Source governance

TADS uses legitimate, documented, licensed or otherwise permitted access. It does not build its acquisition strategy around unauthorized scraping.

Initial sources:

- **Greenhouse** public Job Board GET API
- **Lever** authenticated API access
- permitted company pages and structured public sources through the controlled fetch boundary
- licensed providers through explicit source adapters

Every adapter is subject to source policy, provenance, retention, rate, geographic and privacy controls.

## Security posture

The ingestion boundary treats URLs and retrieved content as hostile. Controls include HTTPS-only fetching, explicit host allowlists, public-address validation, redirect rejection, timeout/byte/content-type budgets, parser constraints and tenant isolation. Application controls are defense in depth; production egress restrictions remain mandatory.

PostgreSQL RLS is not treated as an absolute boundary by itself: PostgreSQL documents that table owners/superusers/BYPASSRLS roles can bypass RLS and that referential-integrity checks bypass row security. TADS therefore requires a trusted application connection boundary and additional cross-tenant integrity checks. https://www.postgresql.org/docs/18/ddl-rowsecurity.html

## Architecture

TADS starts as a modular monolith:

- **Python 3.12+**
- PostgreSQL 17 in CI
- typed domain packages
- transactional migrations with checksums and advisory-lock serialization
- object storage for large immutable source material
- strict HTTP egress policy
- API/worker boundaries introduced only when justified by measured load

A graph database, message broker, universal crawler, ML intent predictor or generic agent layer is **not** introduced simply because it is fashionable.

## Roadmap

**M0** Architecture & Governance → **M1** Intelligence Kernel → **M2** Source Ingestion → **M3** Entity Resolution → **M4** Signal Engine → **M5** Temporal & Correlation → **M6** Account Intelligence → **M7** ICP + Opportunity Engine → **M8** Agent Intelligence → **M9** ReconOS → **M10** FadeReach → **M11** Feedback & Learning → **M12** Console → **M13** Productionization → **M14** Security & Privacy → **M15** Reliability & Scale → **M16** Governance & Compliance → **M17** E2E + Adversarial Validation → **M18** Enterprise GA.

Security, privacy, observability, data quality, testing, evaluation, cost controls and governance are cross-cutting from M0 onward.

## Quality gate

A milestone is not closed until:

- implementation exists on the repository
- domain invariants have executable tests
- migrations are tested against PostgreSQL where applicable
- security and tenant-boundary regressions are covered
- documentation matches the implementation
- CI is green
- the pull request is merged
- the main branch remains green after merge

See `docs/implementation-plan.md`, `docs/architecture/README.md`, `docs/architecture/data-model.md`, `docs/security/threat-model.md`, and `docs/data-source-policy.md`.
