# TADS M0 Threat Model

TADS treats all external content, source metadata, retrieved documents, model output, and third-party tool responses as untrusted.

## Security framework alignment

M0 uses defense-in-depth principles consistent with NIST AI RMF 1.0: Govern, Map, Measure, and Manage are lifecycle functions, with governance cross-cutting the other functions. M0 freezes ownership, trust boundaries, evidence requirements, and risk controls before ingestion and agent execution are introduced. The AI RMF is a risk-management framework rather than a product checklist.

Where TADS later uses LLMs or agents, the threat model also tracks the OWASP 2025 GenAI risks relevant to TADS: prompt injection, sensitive information disclosure, supply-chain risk, data/model poisoning, improper output handling, excessive agency, system prompt leakage, vector/embedding weaknesses, misinformation, and unbounded consumption. These risks do not grant models authority; platform policy and explicit authorization remain authoritative.

## Assets

Provider credentials; tenant/account intelligence; source snapshots and evidence; personal data and contact metadata; entity-resolution decisions; scoring policies/models; agent trajectories and research artifacts; integration credentials.

## Trust boundaries

```
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

Attacker-controlled URLs, redirects and DNS may target internal services. Use scheme allowlists, public-IP validation, redirect revalidation, DNS rebinding defenses, timeout/byte/page budgets, and isolated fetchers. Egress authorization belongs to the fetch boundary, not an LLM.

### Parser/resource exhaustion

Compressed bombs, giant HTML, deep nesting, infinite pagination, and pathological documents can exhaust resources. Enforce byte, depth, time, concurrency, and page-count budgets.

### Prompt injection

Public pages may contain instructions designed to manipulate research agents. Extracted content is data, never authority. Agent Platform policy, tool authorization, and human approval remain authoritative.

### Poisoned intelligence

False articles, copied job postings, stale data, spoofed domains, and contradictory sources can create false signals. Preserve provenance, reliability, temporal metadata, and conflict state. Never convert contradiction into certainty.

### Entity poisoning / false merge

Require multi-feature matching, confidence thresholds, evidence, and review for ambiguous or high-impact merges. Never silently overwrite canonical identity.

### Tenant isolation

Every tenant-scoped query and mutation must enforce server-side tenant context. Cross-tenant reads are security failures and require regression tests.

### Credential leakage

Provider credentials must never enter logs, evidence excerpts, model context, or client responses. Secrets belong in the platform/deployment secret boundary.

### Personal-data overcollection

Prefer company/account-level evidence. Person data is collected only when necessary for an explicitly defined purpose and under applicable legal/provider constraints.

### Supply-chain compromise

Pin and audit dependencies, generate SBOMs at the productionization stage, scan dependencies, and isolate source parsers because they process hostile content.

### Excessive agency and unbounded consumption

Agent capabilities must be least-privileged, bounded by policy, budget, timeout, approval, and tool scopes. Expensive or consequential actions require explicit authorization. TADS domain code never treats model output as authorization.

## M2 implemented controls

The ingestion boundary now enforces HTTPS, explicit provider host allowlists, no URL userinfo, standard-port restrictions, public DNS resolution, redirect rejection, response byte budgets, content-type allowlists, and request timeouts. These are application-layer defenses; production deployment must additionally enforce network egress controls because DNS rebinding and infrastructure-level routing cannot be solved solely in application code.

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

## M0 authoritative references

- NIST AI RMF 1.0: https://www.nist.gov/itl/ai-risk-management-framework
- OWASP GenAI Security Project / Top 10 for LLM Applications: https://genai.owasp.org/llm-top-10/
- OWASP Top 10 Web Application Security Risks: https://owasp.org/Top10/
