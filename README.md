# Tinlance TADS

**Target / Account / Demand Signal Intelligence**

TADS is Tinlance's proprietary intelligence layer for turning fragmented external-world and first-party observations into evidence-backed account intelligence, opportunity hypotheses, prioritization, and recommended action.

## Boundary

TADS answers **who, why, why now, what changed, how confident, what evidence, and what should happen next**.

A signal is evidence of change or context; it is **not** proof of buying intent. TADS does not predict that an account will buy merely because signals exist.

TADS does not send outreach, operate campaigns, replace ReconOS enrichment, or duplicate generic agent infrastructure.

```
External sources
      ↓
Ingestion → normalization → entity resolution
      ↓
Signal + evidence + provenance
      ↓
Temporal correlation / signal stacking
      ↓
Account state
      ↓
Opportunity hypothesis + explainable score
      ↓
Recommendation
      ↓
ReconOS / FadeReach / human decision
```

## M0 status

**Architecture Foundation — implementation complete for M0 contracts and repository gates.**

M0 establishes the domain contract, ownership boundaries, evidence/provenance rules, source governance, persistence/migration invariants, integration ports, threat model, typed contracts, architecture tests, and CI gate.

M0 does **not** claim that the intelligence runtime, PostgreSQL schema, ingestion adapters, entity resolver, signal engine, opportunity engine, agents, ReconOS integration, FadeReach integration, or console are implemented. Those are later milestones.

## Platform boundary

TADS is a domain consumer of `LloydCoder/tinlance-agent-platform`. Generic agent runtime, model/tool routing, authorization, policy, approvals, sandboxing, evidence infrastructure, audit, observability, budgets, and event infrastructure belong to the Agent Platform.

TADS owns intelligence-domain behavior: signals, accounts, entity resolution, temporal correlation, ICP, opportunity scoring, hypotheses, recommendations, and TADS-specific workflows.

The Agent Platform integration remains disabled until a versioned, tested runtime contract is available.

## Non-negotiable principles

- Evidence before inference.
- Unknown is better than fabricated intelligence.
- Signal is not intent.
- Intent is not opportunity.
- Opportunity is not customer.
- Scores are explainable and reproducible.
- Canonical identity changes require evidence and confidence.
- Raw observations are retained separately from normalized intelligence.
- Duplicate observations do not become duplicate signals.
- External web content is hostile input.
- Source legality and provider terms are first-class constraints.
- Personal data is minimized and governed by purpose, provenance, retention, access, and deletion policy.
- TADS never sends outreach.

## M2 status

**Source Ingestion — implementation in progress on the M2 branch.** The controlled fetch boundary now enforces HTTPS, explicit host allowlists, public-address resolution, byte/time/content-type budgets, and redirect rejection. Greenhouse is supported through its documented public Job Board GET API; Lever is supported only through authenticated API access. No universal crawler or LinkedIn automation is introduced.

M2 preserves the M1 evidence chain: source → snapshot → observation. Canonical event creation, entity resolution, signal detection, correlation, and opportunity scoring remain downstream milestones.

## Roadmap

M0 Architecture → M1 Evidence-First Intelligence Kernel → M2 Source Ingestion → M3 Entity Resolution → M4 Signal Detection → M5 Temporal/Correlation Intelligence → M6 Account Intelligence → M7 ICP/Opportunity/Recommendation → M8 Agent Intelligence → M9 ReconOS → M10 FadeReach → M11 Feedback/Outcomes → M12 Console → M13 Productionization → M14 Security/Privacy/Trust → M15 Reliability/Scale → M16 Enterprise Governance → M17 E2E/Adversarial Validation → M18 Enterprise GA/Continuous Assurance.

Security, privacy, observability, testing, data quality, evaluation, cost controls, and documentation are cross-cutting from M0 onward.
