# TADS M0 Canonical Data Model

This is the domain contract for M1. It deliberately separates observations, events, signals, evidence, entities, and derived opportunity state.

## Identity hierarchy

```text
Tenant
 ├── ICPProfile
 ├── MarketSegment / Industry / Geography
 └── Account
      ├── Organization
      ├── Domain
      ├── Person / Role
      ├── Technology / Product
      ├── Relationship
      ├── SignalEvent → Evidence / SourceSnapshot
      ├── SignalCluster
      ├── AccountState / IntentState
      └── Opportunity
             ├── OpportunityHypothesis
             ├── OpportunityScore
             ├── Evidence
             ├── Recommendation
             ├── Action
             └── Feedback / Outcome
```

## Source and observation entities

### Source

Represents a configured source/provider: `id`, tenant scope, kind, name, authority weight, freshness policy, access policy, terms reference, enabled state, and timestamps.

### SourceSnapshot

Immutable observation of source material. It records source, URI, retrieval/publication timestamps, content hash, content type, byte size, storage reference, parser version, sanitized HTTP metadata, and integrity status.

Raw content should live in object storage when large; PostgreSQL stores metadata and references.

### SignalEvent

Canonical representation of a real-world event after normalization/deduplication. It contains a stable event ID, event type/subtype, source observation references, affected entity/account references, occurred/published/observed timestamps, normalized facts, deduplication fingerprint, confidence, and lifecycle status.

One event may have many supporting observations.

## Evidence

Evidence is the auditable support for a claim. It is not equivalent to raw content.

Required concepts include source snapshot, locator, timestamps, extraction method/version, reliability, directness, freshness, confidence, and transformation references. Avoid storing unnecessary personal-data excerpts.

## Account / entity resolution

`Organization` is the canonical legal/business entity. `Account` is the tenant-scoped commercial intelligence view. `Domain` stores normalized internet domains and provenance. `Relationship` stores typed parent/subsidiary/alias/partner/acquisition and similar relationships.

Ambiguous matching uses an explicit `ResolutionCandidate` record. Resolution output includes canonical candidate(s), match features, confidence, supporting evidence, decision method, and whether human review is required.

## Signal

Signals are derived intelligence objects, not raw observations. A signal includes account, taxonomy type/subtype, event, timestamps, source/evidence references, raw and normalized values, confidence, freshness, relevance, uniqueness, reliability, business impact, direction, affected function, related people/technologies, lifecycle status, and taxonomy version.

## SignalCluster

Represents a temporal/semantic stack of related signals. It stores member signals, cluster type, time window, diversity, independence, density, sequence features, confidence, and correlation-rule/model version.

## AccountState

Materialized current state with historical versions. Components include ICP fit, signal strength, intent, momentum, technical need, timing, data confidence, opportunity score, active hypotheses, top drivers, negative factors, recalculation timestamp, and scoring policy version.

## Opportunity

An opportunity is a bounded intelligence conclusion that an account deserves attention. It is not a guaranteed sales opportunity. It stores account, state, status, score, confidence, hypothesis, evidence set, recommendation, capability fit, and lifecycle timestamps.

## OpportunityHypothesis

Must distinguish `observed_facts`, `interpretation`, `potential_problem`, `capability_fit`, `confidence`, `unknowns`, `supporting_evidence`, and `generation_method`. LLM-generated hypotheses are advisory and cannot create facts without evidence.

## Recommendation

Typed action proposal: `IGNORE | MONITOR | RESEARCH | ENRICH | QUEUE_FOR_FADEREACH | REQUEST_HUMAN_REVIEW | CREATE_OPPORTUNITY | EXPAND_RESEARCH`.

Recommendations contain rationale, prerequisites, confidence, expiry, and evidence references.

## Feedback / Outcome

Track `signal → score → recommendation → action → response → meeting → proposal → won/lost → value → retention`. Outcome data is used for evaluation/calibration and never retroactively rewrites what TADS knew at an earlier time.
