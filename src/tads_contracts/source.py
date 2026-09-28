"""Source registry contract."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SourceContract:
    source_id: str
    provider: str
    name: str
    source_class: str
    access_mechanism: str
    terms_reference: str
    permitted_fields: tuple[str, ...]
    geographic_constraints: tuple[str, ...]
    retention_days: int | None
    rate_limit_per_minute: int | None
    authentication_required: bool
    legal_reviewed: bool
    enabled: bool = False

    def validate(self) -> None:
        required = (self.source_id, self.provider, self.name, self.source_class,
                    self.access_mechanism, self.terms_reference)
        if any(not value for value in required):
            raise ValueError("source contract has missing required identity/policy fields")
        if self.retention_days is not None and self.retention_days < 0:
            raise ValueError("retention_days cannot be negative")
        if self.rate_limit_per_minute is not None and self.rate_limit_per_minute <= 0:
            raise ValueError("rate_limit_per_minute must be positive")
        if self.enabled and not self.legal_reviewed:
            raise ValueError("a source cannot be enabled before legal/provider review")
