# Tinlance TADS

**Target / Account / Demand Signal Intelligence**

TADS is Tinlance's proprietary intelligence layer for turning fragmented external-world and first-party signals into evidence-backed account intelligence, opportunity hypotheses, prioritization, and recommended action.

## Boundary

TADS answers **who, why, why now, what changed, how confident, what evidence, and what should happen next**.

It does not send outreach, operate campaigns, replace ReconOS enrichment, or duplicate generic agent infrastructure.

```text
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

## Current status

**M0 — Architecture Foundation: IN PROGRESS**

The repository started empty. M0 establishes the domain contract, platform boundary, provenance requirements, source-policy model, threat model, and staged implementation plan before production code is introduced.

No capability is considered implemented merely because an interface, schema, or placeholder exists.

## Platform boundary

TADS is a domain consumer of `LloydCoder/tinlance-agent-platform`. Generic agent runtime, model/tool routing, authorization, policy, approvals, sandboxing, evidence infrastructure, audit, observability, budgets, and event infrastructure belong to the Agent Platform. TADS owns intelligence-domain behavior: signals, accounts, entity resolution, temporal correlation, ICP, opportunity scoring, hypotheses, recommendations, and TADS-specific workflows.

The current Agent Platform repository is itself at M0 foundation stage and currently contains its architecture contract/README rather than an implemented runtime. TADS therefore records the integration boundary now but will not pretend that platform capabilities are available at runtime until verified.

## Non-negotiable principles

- Evidence before inference.
- Unknown is better than fabricated intelligence.
- A signal is evidence, not buying intent.
- Scores are explainable and reproducible.
- Canonical identity changes require evidence and confidence.
- Raw source observations are retained separately from normalized intelligence.
- Duplicate observations do not become duplicate signals.
- External web content is hostile input.
- Source legality and provider terms are first-class constraints.
- Personal data is minimized and governed by purpose, provenance, retention, access, and deletion policy.
- TADS never sends outreach.

## Roadmap

M0 Architecture → M1 Core Intelligence → M2 Ingestion → M3 Entity Resolution → M4 Signal Engine → M5 Account Intelligence → M6 Opportunity Engine → M7 Agent Intelligence → M8 ReconOS → M9 FadeReach handoff → M10 Feedback → M11 Console → M12 Production Hardening → M13 E2E Validation.
