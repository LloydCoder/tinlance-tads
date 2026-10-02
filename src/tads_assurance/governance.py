"""M16 governance and retention contracts."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetentionPolicy:
    evidence_days: int
    personal_data_days: int
    audit_days: int

    def __post_init__(self) -> None:
        if min(self.evidence_days, self.personal_data_days, self.audit_days) <= 0:
            raise ValueError("retention periods must be positive")
        if self.personal_data_days > self.evidence_days:
            raise ValueError("personal-data retention cannot exceed evidence retention")


@dataclass(frozen=True, slots=True)
class GovernanceRecord:
    control_id: str
    owner: str
    status: str
    reviewed_at: str
    evidence_ref: str
    review_interval_days: int = 90

    def __post_init__(self) -> None:
        if not all((self.control_id, self.owner, self.status, self.reviewed_at, self.evidence_ref)):
            raise ValueError("governance records require owner, status and evidence")
        if self.review_interval_days <= 0:
            raise ValueError("review_interval_days must be positive")
