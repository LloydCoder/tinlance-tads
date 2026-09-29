"""Provider-neutral, validated integration contracts."""

from dataclasses import dataclass\nfrom datetime import datetime


def _bounded(value: float, name: str) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def _identifiers(values: tuple[str, ...], name: str) -> None:
    if not values or any(not value for value in values):
        raise ValueError(f"{name} must contain non-empty identifiers")
    if len(set(values)) != len(values):
        raise ValueError(f"{name} identifiers must be unique")


@dataclass(frozen=True, slots=True)
class EnrichmentRequest:
    account_id: str
    purpose: str
    fields: tuple[str, ...]
    request_id: str | None = None
    evidence_required: bool = True

    def __post_init__(self) -> None:
        if not self.account_id or not self.purpose.strip():
            raise ValueError("account_id and purpose are required")
        if not self.fields or any(not field.strip() for field in self.fields):
            raise ValueError("enrichment fields must be non-empty")
        if any(field.strip() != field for field in self.fields):
            raise ValueError("enrichment fields must be normalized")
        if self.request_id is not None and not self.request_id.strip():
            raise ValueError("request_id cannot be blank")


@dataclass(frozen=True, slots=True)
class EnrichmentResult:
    provider: str
    provider_version: str
    account_id: str
    evidence_ids: tuple[str, ...]
    facts: tuple[tuple[str, str], ...]
    unknowns: tuple[str, ...]
    response_id: str | None = None

    def __post_init__(self) -> None:
        if not self.provider or not self.provider_version or not self.account_id:
            raise ValueError("provider, provider_version and account_id are required")
        _identifiers(self.evidence_ids, "evidence")
        if any(not key.strip() or not value.strip() for key, value in self.facts):
            raise ValueError("enrichment facts must contain non-empty key/value pairs")
        if any(not item.strip() for item in self.unknowns):
            raise ValueError("enrichment unknowns must be non-empty")
        if self.response_id is not None and not self.response_id.strip():
            raise ValueError("response_id cannot be blank")


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
    expires_at: datetime | None = None
    idempotency_key: str | None = None

    def __post_init__(self) -> None:
        if not self.opportunity_id or not self.account_id or not self.hypothesis.strip():
            raise ValueError("handoff identity and hypothesis are required")
        _bounded(self.score, "score")
        _bounded(self.confidence, "confidence")
        _identifiers(self.evidence_ids, "handoff evidence")
        if self.idempotency_key is None or not self.idempotency_key.strip():
            raise ValueError("handoff requires an idempotency key")
