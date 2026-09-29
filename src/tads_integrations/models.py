"""Provider-neutral integration models."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EnrichmentRequest:
    account_id: str
    purpose: str
    fields: tuple[str, ...]
    evidence_required: bool = True


@dataclass(frozen=True, slots=True)
class EnrichmentResult:
    provider: str
    provider_version: str
    account_id: str
    evidence_ids: tuple[str, ...]
    facts: tuple[tuple[str, str], ...]
    unknowns: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OpportunityHandoff:
    opportunity_id: str
    account_id: str
    score: float
    confidence: float
    hypothesis: str
    evidence_ids: tuple[str, ...]
    recommended_persona: str | None
    recommended_angle: str | None
    timing: str | None
