# Provider Capability Contracts

## Purpose

TADS uses provider-neutral ports, but production integrations must bind those ports to an authenticated,
versioned external capability contract. A Python adapter existing in the repository is not proof that the
external provider is available, authorized, compatible or operational.

## M9 — ReconOS

The TADS-side request contract is tads.reconos.v1.

Required request properties:

- tenant identity comes from trusted server-side context, never request free text;
- purpose-limited account enrichment;
- explicit requested fields;
- evidence required by default;
- request ID / idempotency identity;
- authorization decision identifier when available;
- audit correlation identifier when available;
- bounded timeout.

Required response properties:

- matching request ID;
- response ID;
- provider identity and provider version;
- matching schema version;
- target account identity;
- one or more evidence IDs;
- facts represented as typed key/value pairs;
- explicit unknowns.

The ReconOSHttpAdapter enforces HTTPS, exact configured host, standard HTTPS port, no redirects,
bounded response size, bearer authentication, request-id matching and evidence-required responses.

**External verification gate:** the actual ReconOS service must publish an authenticated capability contract
covering endpoint, authentication, scopes, schema/version, rate limits, provenance semantics, error codes,
timeouts and retry behavior. TADS must execute a non-production compatibility test against that service
before M9 is considered operationally complete.

## M10 — FadeReach

The TADS-side handoff contract is tads.fadereach.v1.

Required handoff properties:

- account and opportunity identity;
- bounded score and confidence;
- evidence IDs;
- hypothesis separated from observed evidence;
- recommended persona/angle and timing;
- future timezone-aware expiry;
- idempotency key;
- schema version;
- audit correlation identifier when available.

The FadeReachHttpAdapter is deliberately limited to publishing an intelligence handoff. It has no
email, social, sequence, follow-up, recipient mutation or outreach execution capability.

The adapter enforces HTTPS, exact configured host, standard HTTPS port, no redirects, bounded responses,
bearer authentication, idempotency and response schema validation.

**External verification gate:** the actual FadeReach service must publish an authenticated capability
contract covering endpoint, authentication, scopes, accepted schema/version, idempotency semantics,
rate limits, response identity, expiry behavior and failure/retry semantics. TADS must execute a
non-production compatibility test against that service before M10 is considered operationally complete.

## Release rule

These adapters are safe integration implementations, not permission to invent or assume provider APIs.
A missing or incompatible provider capability fails closed. TADS must not silently downgrade to an
unverified endpoint, scrape an undocumented interface, or treat a successful HTTP response as evidence
without the required provenance fields.
