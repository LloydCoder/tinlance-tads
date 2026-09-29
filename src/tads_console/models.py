"""Evidence-preserving console projection."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AccountIntelligenceView:
    account_id: str
    canonical_name: str
    timeline: tuple[str, ...]
    why_now: tuple[str, ...]
    score: float
    confidence: float
    recommendation: str
    evidence_ids: tuple[str, ...]
    unknowns: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.account_id or not self.canonical_name:
            raise ValueError("account identity is required")
        if not 0.0 <= self.score <= 1.0 or not 0.0 <= self.confidence <= 1.0:
            raise ValueError("score and confidence must be between 0 and 1")
        if not self.evidence_ids:
            raise ValueError("console intelligence views require evidence")
