#!/usr/bin/env python3
"""Fail-closed TADS verification against the canonical TSIC adapter."""

from __future__ import annotations

import json
from urllib.request import Request, urlopen

TSIC_REVISION = "eee3c96d0c7d00fa5441d9509873fbc9e7402edd"
RAW_ROOT = f"https://raw.githubusercontent.com/LloydCoder/tinlance-system-integration/{TSIC_REVISION}"
REQUIRED = {"identity-context", "event-envelope", "delivery-semantics", "trace-context", "economic-attribution"}


def fetch_json(path: str) -> dict:
    request = Request(
        f"{RAW_ROOT}/{path}",
        headers={"Accept": "application/json", "User-Agent": "tinlance-tads-ci"},
    )
    with urlopen(request, timeout=15) as response:
        if response.status != 200:
            raise RuntimeError(f"TSIC contract fetch failed for {path}: HTTP {response.status}")
        return json.load(response)


def main() -> None:
    manifest = fetch_json("manifests/ecosystem.json")
    adapter = fetch_json("integrations/tads/adapter.json")
    registry = fetch_json("catalog/contracts/registry.json")

    system = next(item for item in manifest["systems"] if item["id"] == "tads")
    assert system["repository"] == "LloydCoder/tinlance-tads"
    assert system["governance_role"] == "acquisition_decisioning_authority"

    assert adapter["source_system"] == "tsic"
    assert adapter["target_system"] == "tads"
    assert adapter["status"] == "reference-contract"

    bindings = {item["tsic_contract"] for item in adapter["contract_bindings"]}
    assert bindings == REQUIRED, (sorted(REQUIRED), sorted(bindings))

    registered = {item["id"] for item in registry["contracts"]}
    assert registered >= REQUIRED

    authority = adapter["authority"]
    assert authority["integration_contracts"] == "tsic"
    assert authority["acquisition_targeting"] == "tads"
    assert authority["execution_authority"] == "agent-platform"

    required_invariants = {
        "tads_does_not_grant_execution_authority",
        "evidence_lineage_is_preserved",
        "uncertainty_and_contradictions_are_preserved",
        "tenant_context_is_immutable",
        "replay_is_deterministic",
        "tsic_remains_integration_authority",
        "agent-platform_remains_execution_authority",
    }
    assert set(adapter["invariants"]) == required_invariants

    print(f"PASS TADS TSIC conformance: revision={TSIC_REVISION} contracts={len(bindings)}")


if __name__ == "__main__":
    main()
