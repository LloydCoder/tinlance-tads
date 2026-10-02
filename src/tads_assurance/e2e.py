"""Canonical M17 end-to-end validation trace."""

from dataclasses import dataclass

from .validation import E2EStage


@dataclass(frozen=True, slots=True)
class E2ETrace:
    stages: tuple[E2EStage, ...]
    evidence_ids: tuple[str, ...]

    def validate(self) -> None:
        if self.stages != tuple(E2EStage):
            raise ValueError("E2E trace stages must follow the canonical TADS sequence")
        if not self.evidence_ids:
            raise ValueError("E2E trace requires evidence")
        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("E2E trace evidence identifiers must be unique")
