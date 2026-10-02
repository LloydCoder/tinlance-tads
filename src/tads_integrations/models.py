"""Provider-neutral, validated integration contracts."""

from dataclasses import dataclass
from datetime import UTC, datetime


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
    schema_version: str = "tads.reconos.v1"
    authorization_id: str | None = None
    audit_correlation_id: str | None = None
    timeout_seconds: float = 10.0

    def __post_init__(self) -> None:
        if not self.account_id or not self.purpose.strip():
            raise ValueError("account_id and purpose are required")
        if not self.fields or any(not field.strip() for field in self.fields):
            raise ValueError("enrichment fields must be non-empty")
        if any(field.strip() != field for field in self.fields):
            raise ValueError("enrichment fields must be normalized")
        if self.request_id is not None and not self.request_id.strip():
            raise ValueError("request_id cannot be blank")
        if self.expires_at is None or self.expires_at.tzinfo is None:
            raise ValueError("handoff requires a timezone-aware expiry")
        if self.expires_at <= datetime.now(UTC):
            raise ValueError("handoff expiry must be in the future")
        if not self.schema_version.strip():
            raise ValueError("schema_version is required")
        for value, name in (
            (self.authorization_id, "authorization_id"),
            (self.audit_correlation_id, "audit_correlation_id"),
        ):
            if value is not None and not value.strip():
                raise ValueError(f"{name} cannot be blank")
        if not 0 < self.timeout_seconds <= 60:
            raise ValueError("timeout_seconds must be greater than 0 and at most 60")


@dataclass(frozen=True, slots=True)
class EnrichmentResult:
    provider: str
    provider_version: str
    account_id: str
    evidence_ids: tuple[str, ...]
    facts: tuple[tuple[str, str], ...]
    unknowns: tuple[str, ...]
    response_id: str | None = None
    request_id: str | None = None
    schema_version: str = "tads.reconos.v1"
    received_at: datetime | None = None

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
        if self.request_id is not None and not self.request_id.strip():
            raise ValueError("request_id cannot be blank")
        if not self.schema_version.strip():
            raise ValueError("schema_version is required")
        if self.received_at is not None and self.received_at.tzinfo is None:
            raise ValueError("received_at must be timezone-aware")
        if self.received_at is not None:
            object.__setattr__(self, "received_at", self.received_at.astimezone(UTC))


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
    schema_version: str = "tads.fadereach.v1"
    audit_correlation_id: str | None = None

    def __post_init__(self) -> None:
        if not self.opportunity_id or not self.account_id or not self.hypothesis.strip():
            raise ValueError("handoff identity and hypothesis are required")
        _bounded(self.score, "score")
        _bounded(self.confidence, "confidence")
        _identifiers(self.evidence_ids, "handoff evidence")
        if self.idempotency_key is None or not self.idempotency_key.strip():
            raise ValueError("handoff requires an idempotency key")
        if not self.schema_version.strip():
            raise ValueError("schema_version is required")
        if self.audit_correlation_id is not None and not self.audit_correlation_id.strip():
            raise ValueError("audit_correlation_id cannot be blank")
        if self.expires_at is None or self.expires_at.tzinfo is None:
            raise ValueError("handoff requires a timezone-aware expiry")
        if self.expires_at <= datetime.now(UTC):
            raise ValueError("handoff expiry must be in the future")
