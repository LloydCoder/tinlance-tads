"""Provider-neutral, validated integration contracts."""

from dataclasses import dataclass


def _bounded(value: float, name: str) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


@dataclass(frozen=True, slots=True)
class EnrichmentRequest:
    account_id: str
    purpose: str
    fields: tuple[str, ...]
    evidence_required: bool = True

    def __post_init__(self) -> None:
        if not self.account_id or not self.purpose.strip():
            raise ValueError("account_id and purpose are required")
        if not self.fields or any(not field.strip() for field in self.fields):
            raise ValueError("enrichment fields must be non-empty")
        if any(field.strip() != field for field in self.fields):
            raise ValueError("enrichment fields must be normalized")


@dataclass(frozen=True, slots=True)
class EnrichmentResult:
    provider: str
    provider_version: str
    account_id: str
    evidence_ids: tuple[str, ...]
    facts: tuple[tuple[str, str], ...]
    unknowns: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.provider or not self.provider_version or not self.account_id:
            raise ValueError("provider, provider_version and account_id are required")
        if not self.evidence_ids:
            raise ValueError("enrichment results require evidence")
        if any(not key or not value for key, value in self.facts):
            raise ValueError("enrichment facts must contain non-empty key/value pairs")


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

    def __post_init__(self) -> None:
        if not self.opportunity_id or not self.account_id or not self.hypothesis.strip():
            raise ValueError("handoff identity and hypothesis are required")
        _bounded(self.score, "score")
        _bounded(self.confidence, "confidence")
        if not self.evidence_ids:
            raise ValueError("opportunity handoff requires evidence")
