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
    score_components: tuple[tuple[str, float], ...] = ()
    audit_refs: tuple[str, ...] = ()
    schema_version: str = "tads.console.v1"

    def __post_init__(self) -> None:
        if not self.account_id or not self.canonical_name:
            raise ValueError("account identity is required")
        if not 0.0 <= self.score <= 1.0 or not 0.0 <= self.confidence <= 1.0:
            raise ValueError("score and confidence must be between 0 and 1")
        if not self.evidence_ids:
            raise ValueError("console intelligence views require evidence")
        if not self.score_components:
            raise ValueError("console intelligence views require score decomposition")
        if any(
            not name.strip() or not 0.0 <= value <= 1.0 for name, value in self.score_components
        ):
            raise ValueError("score components must contain bounded named values")
        if len({name for name, _ in self.score_components}) != len(self.score_components):
            raise ValueError("score component names must be unique")
        if not self.schema_version.strip():
            raise ValueError("schema_version is required")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "account_id": self.account_id,
            "canonical_name": self.canonical_name,
            "timeline": list(self.timeline),
            "why_now": list(self.why_now),
            "score": self.score,
            "confidence": self.confidence,
            "score_components": {name: value for name, value in self.score_components},
            "recommendation": self.recommendation,
            "evidence_ids": list(self.evidence_ids),
            "unknowns": list(self.unknowns),
            "audit_refs": list(self.audit_refs),
        }
