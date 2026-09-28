"""Resolution models that preserve ambiguity instead of forcing matches."""

from dataclasses import dataclass
from enum import StrEnum


class ResolutionState(StrEnum):
    MATCHED = "matched"
    PROBABLE = "probable"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class Candidate:
    organization_id: str
    canonical_name: str
    domain: str | None
    name_similarity: float
    domain_exact: bool
    alias_exact: bool
    confidence: float

    def validate(self) -> None:
        if not self.organization_id or not self.canonical_name:
            raise ValueError("candidate requires organization identity")
        if not 0 <= self.name_similarity <= 1:
            raise ValueError("name_similarity must be between 0 and 1")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class ResolutionResult:
    state: ResolutionState
    candidates: tuple[Candidate, ...]
    selected_organization_id: str | None
    rationale: tuple[str, ...]

    def validate(self) -> None:
        if (
            self.state in {ResolutionState.MATCHED, ResolutionState.PROBABLE}
            and not self.selected_organization_id
        ):
            raise ValueError("selected resolution requires an organization")
        if self.state == ResolutionState.AMBIGUOUS and len(self.candidates) < 2:
            raise ValueError("ambiguous resolution requires multiple candidates")
