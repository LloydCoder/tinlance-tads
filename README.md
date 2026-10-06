<div align="center">

# Tinlance TADS

**Target / Account / Demand Signal Intelligence**

Evidence-first account intelligence for engineering-led acquisition teams that need traceable signals, temporal context, bounded opportunity hypotheses, and explainable recommendations.

[![CI](https://github.com/LloydCoder/tinlance-tads/actions/workflows/ci.yml/badge.svg)](https://github.com/LloydCoder/tinlance-tads/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17%2B-4169E1)](https://www.postgresql.org/)

</div>

> [!NOTE]
> TADS is proprietary Tinlance software. Public repository visibility does not grant reuse rights. See [LICENSE](LICENSE).

## Visual overview

```mermaid
flowchart LR
    A[Permitted source] --> B[Snapshot]
    B --> C[Observation]
    C --> D[Canonical event]
    D --> E[Entity / account]
    E --> F[Signal]
    F --> G[Temporal context]
    G --> H[Account state]
    H --> I[Opportunity hypothesis]
    I --> J[Bounded recommendation]
    J --> K[ReconOS enrichment]
    J --> L[FadeReach handoff]
    K --> M[Outcome]
    L --> M
    M --> N[Feedback / evaluation]
```

The diagram reflects the implemented ownership boundary: TADS produces intelligence and bounded handoffs; downstream systems perform their own responsibilities. A real product demo is not currently published, so no fabricated GIF or screenshot is presented as proof.

## Why TADS

TADS is built around reconstructability rather than opaque lead scoring.

| TADS | Boundary |
|---|---|
| Evidence-first | Every material derived result retains evidence lineage. |
| Deterministic core | Core detection, scoring, lifecycle, and evaluation primitives are replayable. |
| Uncertainty-preserving | Unknown, contradictory, ambiguous, and unresolved states remain explicit. |
| Temporal | Publication, effective, observation, detection, first-seen, last-seen, and expiry semantics are distinct. |
| Tenant-aware | PostgreSQL RLS and server-side tenant context provide database-level isolation. |
| Provider-neutral | ReconOS, FadeReach, and Agent Platform remain separately owned systems. |
| Fail-closed | Missing provider evidence or release-gate evidence blocks readiness instead of being inferred. |

TADS is **not** a CRM, universal crawler, LinkedIn scraper, intent oracle, outreach engine, purchase-probability predictor, or second OSINT platform.

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 17+
- Git

Have PostgreSQL running locally and create a database named `tads_test`.

### Five commands

```bash
git clone https://github.com/LloydCoder/tinlance-tads.git && cd tinlance-tads
python -m venv .venv && source .venv/bin/activate
python -m pip install -e '.[dev]'
export DATABASE_URL='postgresql://postgres:postgres@127.0.0.1:5432/tads_test'
python -m tads_db.migrate && python -m pytest
```

For a CI-equivalent run, also execute the formatting, lint, type-check, and dependency-audit commands in [CONTRIBUTING.md](CONTRIBUTING.md).

## Installation

### Editable development install

```bash
python -m pip install -e '.[dev]'
```

### Standard source install

```bash
python -m pip install .
```

### Optional: uv

If you already use [uv](https://docs.astral.sh/uv/):

```bash
uv pip install -e '.[dev]'
```

TADS is currently documented as a source-installable proprietary project; this repository does not claim a public PyPI distribution.

## Usage

TADS is a Python domain library and persistence layer rather than a standalone CLI. The following examples use public package contracts.

### Source-governance example

```python
from tads_contracts import SourceClass, SourceContract
from tads_sources import SourceRecord, SourceRegistry

contract = SourceContract(
    source_id="greenhouse-public-jobs",
    provider="Greenhouse",
    name="Public Job Board",
    source_class=SourceClass.PUBLIC_STRUCTURED,
    access_mechanism="documented public API",
    terms_reference="provider documentation / approved policy",
    permitted_fields=("job_id", "title", "location"),
    geographic_constraints=(),
    retention_days=30,
    rate_limit_per_minute=30,
    authentication_required=False,
    legal_reviewed=True,
    enabled=True,
)

registry = SourceRegistry()
registry.register(SourceRecord(contract=contract))
registry.activate(contract.source_id)

assert registry.ingestion_allowed(contract.source_id)
```

### Deterministic scoring example

```python
from tads_contracts import ScoreComponent, ScoreContract

score = ScoreContract(
    policy_version="demo-v1",
    components=(
        ScoreComponent("signal_strength", 0.8, 0.6, ("evidence-1",)),
        ScoreComponent("timing", 0.7, 0.4, ("evidence-2",)),
    ),
    score=0.76,
    confidence=0.9,
)

score.validate()
assert score.recompute() == 0.76
```

The examples intentionally stop at domain contracts. TADS does not expose an outreach command.

## Configuration

| Setting | Default | Purpose |
|---|---|---|
| Python | 3.12+ | Supported interpreter range |
| PostgreSQL | 17+ | System-of-record and integration-test database |
| `DATABASE_URL` | none | PostgreSQL DSN used by the migration runner and integration tests |
| Install mode | source | Editable or standard local package installation |
| Integration readiness | fail-closed | Unverified ReconOS/FadeReach capabilities do not become active |

Production configuration remains an M13–M18 operational concern. Do not treat local defaults as production configuration.

## Features

| Capability | Status |
|---|---|
| Evidence-first domain contracts | Implemented |
| PostgreSQL migrations and tenant isolation | Implemented |
| Controlled source ingestion | Implemented |
| Ambiguity-preserving entity resolution | Implemented |
| Deterministic signal detection | Implemented |
| Temporal correlation and account intelligence | Implemented |
| Opportunity hypotheses and bounded recommendations | Implemented |
| Governed agent specifications | Implemented |
| ReconOS / FadeReach provider-neutral adapters | Contract-complete; external verification required |
| Alerts, buying windows, graph abstraction, evaluation platform | Implementation-complete |
| Enterprise GA | **Not claimed**; evidence gates remain fail-closed |

## Architecture

The core semantic chain is:

```text
source
→ snapshot
→ observation
→ canonical event
→ entity/account
→ signal
→ temporal context
→ account state
→ opportunity
→ integration handoff
→ outcome
→ feedback
```

Ownership is intentionally split:

- **TADS** — source governance, ingestion, evidence, events, identity resolution, signals, temporal/account intelligence, opportunities, recommendations, alerts, evaluation, and integration contracts.
- **Tinlance Agent Platform** — generic agent runtime, model routing, tool authorization, sandboxing, approvals, generic audit/provenance, memory, budgets, and telemetry.
- **ReconOS** — deep OSINT/enrichment.
- **FadeReach** — engagement execution.
- **SDEA** — acquisition strategy and signal-driven engineering acquisition.

See [architecture](docs/architecture/README.md) for trust boundaries and deployment design.

## Documentation

| Guide | Purpose |
|---|---|
| [Architecture](docs/architecture/README.md) | System planes, trust boundaries, ownership, and deployment |
| [Canonical data model](docs/architecture/data-model.md) | Domain entities and evidence lineage |
| [Integration boundaries](docs/architecture/integration-boundaries.md) | Agent Platform, ReconOS, and FadeReach contracts |
| [Provider capability contracts](docs/architecture/provider-capability-contracts.md) | External verification requirements |
| [Source control plane](docs/architecture/source-control-plane.md) | Source lifecycle and fail-closed eligibility |
| [Data-source policy](docs/data-source-policy.md) | Authorized access, privacy, and prohibited collection |
| [Threat model](docs/security/threat-model.md) | Security threats and required controls |
| [CI hardening](docs/security/ci-hardening.md) | Supply-chain and workflow controls |
| [Implementation plan](docs/implementation-plan.md) | M0–M18 and X1–X8 |
| [Remaining phases](docs/remaining-phases.md) | Operational Enterprise GA gates |
| [llms.txt](llms.txt) | Compact machine-readable documentation map |
| [llms-full.txt](llms-full.txt) | Expanded AI/LLM context pack |

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes. Security reports must follow [SECURITY.md](SECURITY.md).

## License and acknowledgements

TADS is proprietary software owned by Tinlance Limited. See [LICENSE](LICENSE).

The project uses Python, PostgreSQL, Ruff, mypy, pytest, pip-audit, and GitHub Actions. Their respective licenses and terms remain separate from TADS.

<details>
<summary>Release readiness</summary>

M0–M18 implementation/hardening and X1–X8 capability extensions are represented in the repository. That does **not** mean Enterprise GA is deployed.

The remaining release gates include real ReconOS/FadeReach capability verification, production deployment, backup/restore, observability, adversarial validation, load/capacity testing, disaster recovery, privacy/compliance review, and software supply-chain evidence.

See [remaining phases](docs/remaining-phases.md).

</details>

<details>
<summary>Troubleshooting</summary>

**PostgreSQL connection fails**

Confirm PostgreSQL 17+ is running, the `tads_test` database exists, and `DATABASE_URL` points to the correct DSN.

**Integration tests fail locally**

Run migrations first:

```bash
python -m tads_db.migrate
python -m pytest
```

**Dependency audit fails**

Run:

```bash
python -m pip_audit --strict
```

Then review the affected dependency and update the project constraints only after compatibility has been verified.

</details>

<details>
<summary>Support</summary>

See [SUPPORT.md](SUPPORT.md) for issue and commercial support guidance. Vulnerabilities must be reported privately according to [SECURITY.md](SECURITY.md).

</details>
