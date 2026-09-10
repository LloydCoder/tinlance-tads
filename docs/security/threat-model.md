# TADS M0 Threat Model

TADS treats all external content, source metadata, retrieved documents, model output, and third-party tool responses as untrusted.

## Assets

Provider credentials; tenant/account intelligence; source snapshots and evidence; personal data and contact metadata; entity-resolution decisions; scoring policies/models; agent trajectories and research artifacts; integration credentials.

## Trust boundaries

```text
Internet / third-party source
        │ hostile/untrusted
        ▼
Fetcher sandbox
        │ validated content
        ▼
Parser / extractor
        │ normalized candidate
        ▼
TADS domain
        │ authenticated tenant context
        ▼
PostgreSQL / object storage
        │ governed integration
        ├── Agent Platform
        ├── ReconOS
        └── FadeReach
```

## Primary threats and controls

### SSRF / egress abuse

Attacker-controlled URLs, redirects and DNS may target internal services. Use scheme allowlists, public-IP validation, redirect revalidation, DNS rebinding defenses, timeout/byte/page budgets, and isolated fetchers.

### Parser/resource exhaustion

Compressed bombs, giant HTML, deep nesting, infinite pagination, and pathological documents can exhaust resources. Enforce byte, depth, time, concurrency, and page-count budgets.

### Prompt injection

Public pages may contain instructions designed to manipulate research agents. Extracted content is data, never authority. Agent Platform policy and tool authorization remain authoritative.

### Poisoned intelligence

False articles, copied job postings, stale data, spoofed domains, and contradictory sources can create false signals. Preserve provenance, reliability, temporal metadata, and conflict state. Never convert contradiction into certainty.

### Entity poisoning / false merge

Require multi-feature matching, confidence thresholds, evidence, and review for ambiguous/high-impact merges.

### Tenant isolation

Every tenant-scoped query and mutation must enforce server-side tenant context. Cross-tenant reads are security failures and require regression tests.

### Credential leakage

Provider credentials must never enter logs, evidence excerpts, model context, or client responses. Secrets belong in the platform/deployment secret boundary.

### Personal-data overcollection

Prefer company/account-level evidence. Person data is collected only when necessary for an explicitly defined purpose and under applicable legal/provider constraints.

### Supply-chain compromise

Pin and audit dependencies, generate SBOMs, scan dependencies, and isolate source parsers because they process hostile content.

## Required controls before M2

- strict URL parser and egress policy
- fetch budgets
- content-type and size validation
- sandbox/isolation strategy
- SSRF regression suite
- prompt-injection regression fixtures
- secret redaction
- tenant context contract
- provenance schema
- retention/deletion policy
- source terms registry

Security heuristics may flag, quarantine, redact, or request review. They must not silently become authorization; authorization belongs to the platform/control boundary.
