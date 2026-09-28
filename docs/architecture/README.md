# TADS Architecture — M0

## Mission

TADS converts external-world and first-party observations into an auditable chain:

`source observation → canonical event → signal → resolved account/entity → correlated account state → opportunity hypothesis → explainable score → recommendation`

The system must preserve enough evidence to reconstruct why an intelligence claim exists.

## Domain boundary

### TADS owns

- Source registry and TADS ingestion contracts
- Raw observation normalization
- Canonical event construction and deduplication
- Entity resolution and account identity
- Signal taxonomy and signal lifecycle
- Temporal decay and signal stacking
- Account state and intelligence timelines
- Configurable ICP profiles
- Opportunity hypotheses
- Explainable opportunity scoring
- Recommendations and feedback/outcome models
- TADS-specific research workflows and agents

### Agent Platform owns

- Agent runtime and orchestration
- Model/provider routing
- Tool execution boundary
- Identity and authorization primitives
- Policy enforcement
- Human approval primitives
- Sandbox/isolation primitives
- Generic evidence/provenance/audit infrastructure
- Generic eventing/outbox infrastructure
- Memory/retrieval primitives
- Budgets, telemetry, trajectory and platform security controls

The Agent Platform repository currently documents these boundaries but contains only its README on `main`; therefore TADS integration is initially represented by provider-neutral ports and capability checks, not assumed runtime dependencies.

### ReconOS owns

Deep OSINT/enrichment and relationship/technical intelligence. TADS requests enrichment through an adapter; it does not reimplement ReconOS.

### FadeReach owns

Research-to-outreach execution. TADS may publish an opportunity handoff containing account context, evidence, score, hypothesis, recommended persona/angle, and timing. TADS never sends outreach or runs sequences.

## Logical planes

```text
SOURCE PLANE
source registry → fetch policy → fetcher → validation → raw observations
                                      ↓
INTELLIGENCE PLANE
normalization → event identity → entity resolution → signals → evidence
                                      ↓
ACCOUNT PLANE
account timeline → temporal state → signal stacking → ICP fit
                                      ↓
OPPORTUNITY PLANE
hypothesis → score → confidence → explanation → recommendation
                                      ↓
INTEGRATION PLANE
ReconOS enrichment → human review → FadeReach handoff

CROSS-CUTTING CONTROL PLANE
tenant → authorization → policy → provenance → audit → observability → retention
```

## Processing contract

1. Fetch — obtain permitted source material under source-specific policy.
2. Validate — enforce URL, content type, size, redirect, timeout, encoding, and parser constraints.
3. Observe — store immutable raw observation metadata and content reference.
4. Normalize — convert source-specific records to canonical event candidates.
5. Resolve — map candidates to canonical entities/accounts with explicit confidence and evidence.
6. Classify — map canonical events to one or more signal taxonomy nodes.
7. Deduplicate — collapse repeated observations of the same real-world event while retaining all supporting sources.
8. Correlate — build temporal relationships and signal stacks.
9. Score — compute deterministic, versioned, explainable components.
10. Hypothesize — produce bounded interpretations that distinguish observed facts from inference.
11. Recommend — select an action based on score, confidence, freshness, policy, and tenant configuration.

## Intelligence graph

PostgreSQL is the initial system of record. Graph behavior is represented through relational entities and relationship tables rather than introducing a graph database prematurely.

Core nodes:

`Tenant, Account, Organization, Domain, Person, Role, Technology, Product, Signal, SignalSource, SignalEvent, SignalCluster, AccountState, IntentState, Opportunity, OpportunityHypothesis, OpportunityScore, ICPProfile, MarketSegment, Industry, Geography, Evidence, Source, SourceSnapshot, Relationship, Recommendation, Action, Feedback, Outcome`

A graph database can be introduced only when measured query patterns demonstrate a need that PostgreSQL cannot meet economically.

## Evidence invariant

Every material intelligence claim must reference one or more evidence records. Evidence records identify source, source URL/provider reference, timestamps, extraction method/version, content hash or immutable object reference, relevant locator, source reliability metadata, transformation lineage, and confidence.

Scores and hypotheses are derived artifacts and must reference the inputs used to produce them.

## Temporal model

TADS stores `published_at`, `effective_at`, `observed_at`, `detected_at`, `first_seen`, `last_seen`, and optional `expires_at`. Temporal decay is configurable by signal type and versioned with the scoring policy.

A job posting disappearing does not automatically mean a hire occurred. Absence is modeled separately from affirmative evidence.

## Scoring architecture

MVP scoring is deterministic and versioned. It combines ICP fit, signal strength, recency, reliability, diversity, density, momentum, technical need, strategic relevance, timing, historical engagement, and capability fit.

The implementation must return component values and evidence references. Later statistical/ML models are additional scoring layers, not replacements for the auditable baseline.

## Multi-tenancy

All domain records are tenant-scoped unless explicitly classified as immutable global reference data. Tenant identity is resolved server-side and must never be trusted from model output or client-provided free text alone.

Initial deployment uses the Tinlance internal tenant. The schema remains SaaS-ready from M1 onward.

## Deployment posture

Start as a modular monolith with API + worker boundaries. PostgreSQL is the durable store and initial event/outbox mechanism. Add a broker only after throughput or isolation measurements justify it.

Recommended initial runtime: Python 3.12+, FastAPI at the API boundary only, PostgreSQL, a typed migration layer, async HTTP with strict egress policy, object storage for large evidence, OpenTelemetry-compatible instrumentation, and containerized API/worker deployment.

No production dependency on the Agent Platform is claimed until that repository exposes a tested integration surface.
