# TADS Implementation Plan

## M0 — Architecture Foundation

Status: **PARTIALLY IMPLEMENTED**

Completed in this branch:

- repository boundary established
- Agent Platform/TADS ownership boundary documented
- canonical intelligence pipeline defined
- canonical data model defined
- provenance/evidence invariant defined
- temporal model defined
- source governance model defined
- initial threat model defined
- staged roadmap defined

Remaining M0 work:

1. Verify the Agent Platform's concrete integration contracts as they are implemented.
2. Define the versioned source, taxonomy, scoring, and provenance contracts as typed code.
3. Establish repository CI and security gates.
4. Establish the database/migration baseline.
5. Add architecture/contract tests that prevent boundary drift.
6. Define adapter contracts for ReconOS and FadeReach without implementing those systems inside TADS.

## M1 — Core Intelligence Domain

- tenant/account/entity schema
- sources and source snapshots
- evidence/provenance references
- signal events/signals
- relationships
- deterministic API schemas
- migration and repository tests

## M2 — Ingestion

Start with controlled public structured sources and first-party data. Greenhouse Job Board and Lever public postings are strong initial job-signal candidates because their vendors document public job-posting interfaces. Add company pages/news only behind the hardened fetcher boundary.

## M3 — Entity Resolution

- normalization
- domain/legal-name/alias matching
- relationship graph
- confidence and ambiguity states
- golden resolution dataset
- false-merge regression tests

## M4 — Signal Engine

- taxonomy
- event canonicalization
- deduplication
- temporal decay
- stacking/correlation
- deterministic signal quality model

## M5 — Account Intelligence

- account timeline
- account state materialization
- hiring/technology/market intelligence views
- explainable state drivers

## M6 — Opportunity Engine

- configurable ICP
- deterministic opportunity score
- confidence
- evidence-backed hypothesis
- negative factors
- recommendation engine

## M7 — Agent Intelligence

Agents are introduced only where they outperform deterministic code. Agent Platform is the execution/control substrate; TADS owns domain-specific tools, prompts/specifications, evidence requirements, and evaluations.

## M8 — ReconOS

Request enrichment and consume returned evidence. No duplicate OSINT engine.

## M9 — FadeReach

Publish a versioned opportunity handoff. No outreach execution in TADS.

## M10 — Feedback

Capture action/outcome data, evaluate signal quality and calibration, and prevent outcome leakage into historical state.

## M11 — Console

Account intelligence, timeline, why-now explanation, evidence, hypotheses, score decomposition, and recommendations.

## M12 — Production Hardening

Tenant isolation, retention/deletion, egress controls, performance, observability, disaster recovery, dependency/security gates, deployment validation.

## M13 — End-to-end validation

Prove with real permitted evidence:

`source → observation → event → entity → account → signal → context → score → hypothesis → recommendation → handoff`

Completion requires tests and runtime evidence, not documentation alone.
