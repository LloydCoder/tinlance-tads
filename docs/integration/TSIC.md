# TSIC integration

TADS consumes the canonical TSIC ecosystem contract while retaining authority over targeting, account intelligence and acquisition decisioning.

## Boundary

- **TSIC** owns ecosystem integration contracts, compatibility and certification.
- **TADS** owns source governance, evidence lineage, signals, temporal account state, opportunity hypotheses and bounded recommendations.
- **ReconOS** owns deep OSINT/enrichment.
- **FadeReach** owns outreach execution.
- **Agent Platform** owns consequential agent execution authority.

The canonical acquisition path is:

`World Intelligence → TADS → SDEA → ReconOS → FadeReach`

TADS produces intelligence and bounded handoffs; it does not grant execution permission.

## Conformance

Run:

```bash
python scripts/tsic_conformance.py
```

The check consumes the immutable TSIC revision declared in the script and validates the canonical TADS adapter, contract registry, repository mapping and authority invariants.

Passing the gate proves compatibility with the reviewed TSIC contract surface; it does not claim external production deployment.

## Evidence rule

Every material TADS output must preserve evidence lineage and uncertainty. Signals are intelligence, not ground truth and never become execution authority.
