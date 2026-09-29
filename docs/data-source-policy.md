# TADS Data Source Policy

## Principle

A source being publicly reachable does **not** automatically mean it is authorized for automated collection, reuse or redistribution.

TADS uses legitimate, documented, licensed or otherwise permitted access and records the governing constraints before activating an adapter.

## Source classes

### Tier A — first-party/authenticated

Customer-authorized systems, Tinlance-owned properties and authenticated provider APIs. Access is tenant-scoped and purpose-limited.

### Tier B — documented structured APIs

**Greenhouse:** use documented public Job Board GET endpoints for public job-board data.

**Lever:** use the documented authenticated API surface; TADS does not claim anonymous Lever API access. Credentials must be least privileged and protected.

Provider API behavior, terms and limits are revalidated before production releases.

### Tier C — permitted public pages

Company career pages, public press releases, public documentation, public changelogs, public status pages and similar sources where automated access and reuse are permitted.

### Tier D — licensed providers

Commercial technographic, market, news or intent data. Contract metadata must include permitted use, redistribution, retention, geography, fields and deletion obligations.

## Prohibited by default

- unauthorized automated access
- bypassing authentication/access controls
- circumventing rate limits, CAPTCHAs or technical barriers
- LinkedIn scraping or automated activity without explicit authorized access
- leaked/stolen/unlawfully disclosed datasets
- sensitive personal-data collection without documented lawful purpose and controls

## Source registry contract

Every adapter records:

`provider, source_kind, access_method, terms_reference, allowed_fields, geography, retention, rate_limit, authentication, reliability, privacy_review, adapter_version`

A disabled or expired source cannot be fetched.

## Evidence and provenance

Every source snapshot carries source identity, retrieval time, URL/provider reference, content hash, parser/extraction version and integrity metadata.

Conflicting sources remain conflicting. A model can summarize evidence but cannot invent absent facts.

## Personal data

Prefer account/company evidence. Where person-level data is necessary, apply purpose limitation, minimization, accuracy, storage limitation, access control and deletion/objection mechanisms. Legal basis and provider terms must be evaluated for the particular processing context.

## Operational rule

When source legality or authorization is uncertain, **do not fetch**. Quarantine the source configuration for human/legal review rather than turning uncertainty into an ingestion decision.
