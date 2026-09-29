"""Opportunity-domain models."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ICPProfile:
    industries: frozenset[str]
    geographies: frozenset[str]
    min_employees: int = 0
    max_employees: int | None = None
    required_capabilities: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if self.min_employees < 0:
            raise ValueError("min_employees cannot be negative")
        if self.max_employees is not None and self.max_employees < self.min_employees:
            raise ValueError("max_employees cannot be below min_employees")


@dataclass(frozen=True, slots=True)
class OpportunityResult:
    account_id: str
    icp_fit: float
    evidence_strength: float
    timing: float
    negative_factor: float
    score: float
    confidence: float
    hypothesis: str
    recommendation: str
    reasons: tuple[str, ...]
    unknowns: tuple[str, ...]
    evidence_ids: tuple[str, ...]
