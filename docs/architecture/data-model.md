# TADS Canonical Data Model

This document is the canonical domain contract. Physical schemas may evolve through migrations, but semantic distinctions in this document are non-negotiable.

## Identity and tenancy

```
Tenant
 ├─ ICPProfile
 ├─ Market / Industry / Geography
 └─ Account
     ├─ Organization
     ├─ Domain
     ├─ Relationship
     ├─ Signal
     ├─ AccountState
     └─ Opportunity
```

**Organization** is the canonical real-world business identity. **Account** is the tenant-specific commercial intelligence view. The two must not be conflated.

## Source → observation

**Source** identifies a provider/access contract: authority, access mechanism, terms, allowed fields, rate limits, geographic constraints, retention and reliability profile.

**SourceSnapshot** is immutable retrieved source material metadata: source, URI, content hash, content type, byte size, retrieval time, publication time when known, parser version, storage reference and integrity status.

**Observation** records what was actually observed from a snapshot. Observation is not yet a signal and does not imply intent.

## Canonical event

A **CanonicalEvent** represents a normalized real-world change. Multiple observations can support one event.

Required concepts:

- stable event identity
- event type/subtype
- affected organization/account
- observed/published/effective timestamps
- normalized facts
- deduplication fingerprint
- supporting observations
- confidence/lifecycle
- policy/version

Absence is never silently converted into an affirmative event.

## Entity resolution

Resolution is a decision process:

`input identity → candidates → features → confidence → decision`

Allowed states:

- **MATCHED** — sufficient evidence for deterministic selection
- **PROBABLE** — strong candidate but not equivalent to certainty
- **AMBIGUOUS** — multiple plausible candidates or insufficient separation
- **UNRESOLVED** — no candidate meets the candidate-generation floor
- **REJECTED** — candidate is explicitly excluded by policy/evidence

Candidate features may include exact normalized domain, exact alias, normalized-name similarity, geographic context, source context and relationship evidence.

A false merge is more damaging than an unresolved entity. High-impact merges require evidence and, where configured, human review.

## Signal

A **Signal** is derived from an observation/canonical event and must carry evidence references.

Current M4 taxonomy is intentionally small:

- company
- hiring
- technology
- product
- security
- regulatory
- digital
- commercial

A signal also has subtype, lifecycle state, taxonomy version, strength, freshness, reliability, quality, direction, relevance, business impact and rationale.

**Signal quality is not purchase probability.**

## Temporal context

TADS distinguishes:

- `published_at` — source publication time
- `effective_at` — when the real-world change took effect, if known
- `observed_at` — when TADS observed it
- `detected_at` — when TADS classified it
- `first_seen_at` / `last_seen_at` — source observation boundaries
- `expires_at` — explicit validity end, when known

A disappearance is absence evidence, not proof of the opposite event.

## Account state

Account state is a materialized, versioned view of evidence and context. It may include ICP fit, signal strength/diversity, momentum, technical need, timing, negative evidence, data confidence, opportunity state and top drivers.

## OpportunityHypothesis

`OpportunityHypothesis` is the bounded, evidence-backed interpretation attached to an opportunity.

## Opportunity hypothesis

Every hypothesis separates:

- observed facts
- interpretation
- potential problem
- capability fit
- confidence
- unknowns
- supporting evidence
- generation method/version

LLM-generated interpretations cannot create facts.

## Recommendation

`IGNORE | MONITOR | RESEARCH | ENRICH | QUEUE_FOR_FADEREACH | REQUEST_HUMAN_REVIEW | CREATE_OPPORTUNITY | EXPAND_RESEARCH`

Recommendations include rationale, prerequisites, confidence, expiry and evidence references.

## Outcome

Outcome data follows:

`signal → score → recommendation → action → response → meeting → proposal → won/lost → value/retention`

Outcome data must not retroactively alter what TADS knew at the time of the decision.


## Integration and feedback entities

**EnrichmentRun** records a purpose-limited request/result boundary to ReconOS. It carries provider/version, requested fields, evidence references, facts and unknowns. It is append-only and tenant-scoped.

**OpportunityHandoff** records the exact opportunity, account, score, confidence, bounded hypothesis, evidence and recommended engagement context sent toward FadeReach. It is not an outreach instruction and TADS never executes outreach.

Normalized evidence-link tables are authoritative for lineage; JSON evidence identifiers are retained as a portable snapshot of the handoff/enrichment payload.

## Materialized intelligence lineage\n\nTemporal correlations, account states and opportunities retain explicit normalized evidence links in addition to their derived numeric values. Their repository contracts reject evidence-free materialized intelligence. This prevents an aggregate score or state from becoming a self-authenticating fact.\n\n## Outcome and governance contracts

M11 outcomes are appended after the decision. They never mutate historical signals, scores or recommendations. Evaluation joins outcomes to the frozen decision-time policy/version.

M16 governance records bind a control to an owner, review state, review time and evidence reference. Retention policies are explicit and fail closed on invalid periods.

## Assurance

M13 readiness, M17 E2E validation and M18 enterprise readiness are derived states. A readiness result is **blocked** when any required control is absent; no partial readiness is promoted to production status.
