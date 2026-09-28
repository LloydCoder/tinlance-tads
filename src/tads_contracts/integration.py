"""Provider-neutral ReconOS and FadeReach ports."""
from dataclasses import dataclass
from typing import Protocol, Sequence

@dataclass(frozen=True, slots=True)
class ReconOSRequest:
    request_id: str
    tenant_id: str
    account_id: str
    requested_domains: tuple[str, ...]
    purpose: str

@dataclass(frozen=True, slots=True)
class FadeReachHandoff:
    handoff_id: str
    tenant_id: str
    account_id: str
    opportunity_id: str
    why_now: str
    evidence_ids: tuple[str, ...]
    recommended_angle: str | None
    expires_at: str | None

class ReconOSPort(Protocol):
    def request_enrichment(self, request: ReconOSRequest) -> str:
        """Return an external request/reference ID."""

class FadeReachPort(Protocol):
    def publish_handoff(self, handoff: FadeReachHandoff) -> str:
        """Publish intelligence only; never execute outreach."""

def require_evidence(evidence_ids: Sequence[str]) -> tuple[str, ...]:
    result = tuple(evidence_ids)
    if not result:
        raise ValueError("integration handoffs require evidence")
    return result
