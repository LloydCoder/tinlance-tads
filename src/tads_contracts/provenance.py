"""Evidence and lineage contracts."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ProvenanceRef:
    source_id: str
    snapshot_id: str
    content_hash: str
    observed_at: datetime
    extractor: str
    extractor_version: str
    locator: str | None = None

    def validate(self) -> None:
        if not self.source_id or not self.snapshot_id or not self.content_hash:
            raise ValueError("provenance requires source, snapshot and content hash")
        if not self.extractor or not self.extractor_version:
            raise ValueError("provenance requires extractor identity and version")


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    evidence_id: str
    provenance: ProvenanceRef
    confidence: float

    def validate(self) -> None:
        self.provenance.validate()
        if not self.evidence_id:
            raise ValueError("evidence_id is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("evidence confidence must be between 0 and 1")
