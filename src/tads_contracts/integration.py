"""Compatibility aliases for the canonical M9/M10 integration contracts.

The canonical integration models live in tads_integrations. This module remains as
a stable M0 import surface while preventing two independent contract models from
drifting apart.
"""

from collections.abc import Sequence

from tads_integrations import EnrichmentRequest, OpportunityHandoff

ReconOSRequest = EnrichmentRequest
FadeReachHandoff = OpportunityHandoff


def require_evidence(evidence_ids: Sequence[str]) -> tuple[str, ...]:
    result = tuple(evidence_ids)
    if not result or any(not item for item in result):
        raise ValueError("integration handoffs require non-empty evidence identifiers")
    if len(set(result)) != len(result):
        raise ValueError("integration evidence identifiers must be unique")
    return result


__all__ = ["FadeReachHandoff", "ReconOSRequest", "require_evidence"]
