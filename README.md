# Tinlance TADS

**Target / Account / Demand Signal Intelligence**

TADS is Tinlance's evidence-first account-intelligence substrate. It converts permitted observations into traceable signals, temporal context, account state, bounded opportunity hypotheses and explainable recommendations.

> **Who matters? What changed? Why does it matter? Why now? What evidence supports that conclusion? What is still unknown?**

TADS is deliberately **not** a CRM, lead database, universal crawler, intent oracle or outreach engine.

## Architecture

```
permitted sources
      │
      ▼
M2 controlled ingestion
      │
      ▼
M3 entity resolution
      │
      ▼
M4 signals ──► M5 temporal/correlation
      │                 │
      └────────┬────────┘
               ▼
        M6 account state
               │
               ▼
        M7 opportunity
               │
        ┌──────┴──────┐
        ▼             ▼
     M9 ReconOS    M10 FadeReach
     enrichment    handoff only
        │             │
        └──────┬──────┘
               ▼
          M11 outcomes
               │
               ▼
      M12–M18 assurance
```

### Ownership boundaries

**TADS owns:** source policy and adapters, observations, entity resolution, signals, temporal reasoning, account state, ICP, opportunity hypotheses, recommendations, feedback and TADS-specific research workflows.

**Agent Platform owns:** generic agent runtime, model routing, tool authorization, sandboxing, approvals, generic audit/provenance, memory/retrieval and platform telemetry.

**ReconOS owns:** deep enrichment/OSINT. TADS requests purpose-limited enrichment and consumes evidence; it does not duplicate ReconOS.

**FadeReach owns:** engagement execution. TADS publishes a versioned opportunity handoff and never sends outreach.

## Non-negotiable invariants

1. Observation ≠ signal.
2. Signal ≠ intent.
3. Intent ≠ opportunity.
4. Opportunity ≠ customer.
5. Evidence ≠ interpretation.
6. Unknown beats fabrication.
7. Ambiguity beats a false entity merge.
8. Material intelligence is reconstructable to evidence.
9. Tenant identity is established by trusted server-side context.
10. External content and model output are untrusted data, never authorization.

## Milestone status

| Milestone | Status | Executable scope |
|---|---|---|
| M0 | ✅ Complete | Architecture, governance, boundaries and typed contracts |
| M1 | ✅ Complete | PostgreSQL evidence-first kernel, RLS, tenant isolation and immutable evidence |
| M2 | ✅ Complete | Controlled source ingestion and provenance |
| M3 | ✅ Complete | Conservative entity resolution with ambiguity preservation |
| M4 | ✅ Complete | Deterministic signal taxonomy/detection and evidence lineage |
| M5 | ✅ Complete | Temporal/correlation feature kernel |
| M6 | ✅ Complete | Explainable account-state derivation |
| M7 | ✅ Complete | Deterministic ICP/opportunity scoring and recommendations |
| M8 | ✅ Complete | Governed agent specifications; execution remains Agent Platform-owned |
| M9 | 🚧 Contract-complete | Provider-neutral ReconOS request/result contract plus evidence-backed persistence |
| M10 | 🚧 Contract-complete | Evidence-backed FadeReach opportunity handoff; no outreach execution |
| M11 | 🚧 Contract-complete | Append-only outcomes, precision/recall and confidence calibration primitives |
| M12 | 🚧 Contract-complete | UI-neutral account intelligence/readiness contract; console remains a separate application surface |
| M13 | 🚧 Contract-complete | Runtime readiness contract; deployment infrastructure remains environment-specific |
| M14 | 🚧 Contract-complete | Fail-closed security/privacy policy contract |
| M15 | 🚧 Contract-complete | Bounded deterministic retry/reliability policy |
| M16 | 🚧 Contract-complete | Governance ownership, review and retention contracts |
| M17 | 🚧 Contract-complete | Closed canonical E2E stage validation contract |
| M18 | 🚧 Contract-complete | Fail-closed enterprise GA gate |

**Contract-complete does not mean production-deployed.** External provider adapters, cloud infrastructure, legal review, load tests, disaster recovery evidence and operational controls are release gates and are intentionally not fabricated.

## Evidence chain

`source → snapshot → observation → canonical event → entity/account → signal → correlation → account state → opportunity → integration handoff → outcome → feedback`

Every derived artifact must retain the policy/taxonomy/version and input references needed for deterministic replay.

## Data-source policy

Public reachability is not authorization. TADS permits documented, licensed, customer-authorized or otherwise lawful access and explicitly prohibits bypassing authentication, CAPTCHAs, rate limits or technical barriers.

Initial adapters include documented Greenhouse public Job Board access and authenticated Lever access. Source activation remains subject to terms, purpose, geography, retention, privacy and rate-limit review.

## Security

The ingestion boundary treats URLs and retrieved content as hostile. Application controls include HTTPS/host restrictions, public-address validation, redirect rejection, size/time/content-type budgets and tenant isolation. Production egress controls remain mandatory.

PostgreSQL RLS is defense in depth, not the sole tenant boundary: owners and BYPASSRLS roles can bypass RLS, and referential-integrity checks bypass row security. The application therefore uses a least-privileged role plus explicit tenant-parent integrity checks.

The security program is aligned with OWASP Top 10:2025 and agentic-AI guidance, especially access control, supply-chain integrity, injection, insecure design, data integrity, logging and excessive agency.

## Technology

- Python 3.12+
- PostgreSQL 17+ (CI currently uses PostgreSQL 17)
- typed modular-monolith architecture
- transactional, checksummed migrations
- object storage for large immutable source material
- strict network egress policy
- API/worker separation only when measured load requires it

## Quality gate

A milestone is closed only when:

- implementation exists
- invariants have executable tests
- PostgreSQL behavior is tested where applicable
- tenant/security regressions are covered
- documentation matches code
- CI is green
- the change is merged
- main is green after merge

See `docs/implementation-plan.md`, `docs/remaining-phases.md`, `docs/architecture/README.md`, `docs/architecture/data-model.md`, `docs/security/threat-model.md` and `docs/data-source-policy.md`.
