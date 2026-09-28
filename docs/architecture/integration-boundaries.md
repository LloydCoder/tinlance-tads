# TADS Integration Boundaries — M0

## Purpose

Freeze ownership and call direction before product integrations are implemented.

## Agent Platform

TADS consumes the Agent Platform as a control and execution substrate. TADS must not reimplement model routing, generic tool execution, identity, authorization, approvals, sandboxing, generic provenance/audit, memory, budgets, or platform observability.

The current platform repository does not expose a verified runtime API. M0 therefore defines provider-neutral ports only. An integration becomes enabled only after a versioned platform contract is implemented, tested, authenticated, and compatibility-checked.

## ReconOS

TADS may request enrichment for an account and consume returned evidence. ReconOS owns deep OSINT/enrichment. TADS must not embed a second OSINT/crawling engine under the name of integration.

Future adapter requirements:
- tenant-scoped identity
- explicit purpose
- request and response IDs
- evidence/provenance references
- timeout and retry policy
- authorization decision
- audit correlation ID
- schema version

## FadeReach

TADS may publish an intelligence handoff containing account context, why-now explanation, evidence references, opportunity hypothesis, score/explanation, recommended persona/angle, and expiry.

TADS must not send email, automate social activity, create outreach sequences, manage follow-ups, or impersonate a salesperson.

Future adapter requirements:
- tenant-scoped identity
- immutable handoff ID
- schema version
- evidence references
- explicit expiry
- idempotency key
- audit correlation ID

## Directionality

TADS to Agent Platform is a controlled dependency.
TADS to ReconOS is an enrichment request.
TADS to FadeReach is an intelligence handoff.

Neither downstream product may silently mutate TADS evidence or historical intelligence. Writes must be explicit, authenticated, versioned, and auditable.
