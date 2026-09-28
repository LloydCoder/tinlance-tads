"""Deterministic, explainable scoring contract."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ScoreComponent:
    name: str
    value: float
    weight: float
    evidence_ids: tuple[str, ...]

    def validate(self) -> None:
        if not self.name:
            raise ValueError("score component name is required")
        if not 0.0 <= self.value <= 1.0:
            raise ValueError("score component value must be between 0 and 1")
        if self.weight < 0:
            raise ValueError("score component weight cannot be negative")
        if not self.evidence_ids:
            raise ValueError("every score component must reference evidence")

@dataclass(frozen=True, slots=True)
class ScoreContract:
    policy_version: str
    components: tuple[ScoreComponent, ...]
    score: float
    confidence: float

    def validate(self) -> None:
        if not self.policy_version:
            raise ValueError("score policy version is required")
        if not 0 <= self.score <= 1:
            raise ValueError("score must be between 0 and 1")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        for component in self.components:
            component.validate()
