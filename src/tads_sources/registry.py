"""Fail-closed source registry and lifecycle controls.

The registry governs whether a source may participate in ingestion. It does not
fetch data and therefore does not duplicate tads_ingest.
"""

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from tads_contracts.source import SourceContract


class SourceLifecycle(StrEnum):
    REGISTERED = "registered"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    RETIRED = "retired"


class SourceHealth(StrEnum):
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class SourceRecord:
    contract: SourceContract
    lifecycle: SourceLifecycle = SourceLifecycle.REGISTERED
    health: SourceHealth = SourceHealth.UNKNOWN
    last_success_at: datetime | None = None
    last_failure_at: datetime | None = None
    connector_version: str = "unknown"

    def validate(self) -> None:
        self.contract.validate()
        if not self.connector_version:
            raise ValueError("connector_version is required")
        for value in (self.last_success_at, self.last_failure_at):
            if value is not None and value.tzinfo is None:
                raise ValueError("source health timestamps must be timezone-aware")
        if self.lifecycle is SourceLifecycle.ACTIVE and (
            not self.contract.enabled or not self.contract.legal_reviewed
        ):
            raise ValueError("an active source must be enabled and legally reviewed")
        if self.lifecycle is SourceLifecycle.RETIRED and self.contract.enabled:
            raise ValueError("a retired source cannot remain enabled")


class SourceRegistry:
    """In-memory source control plane; persistence belongs to tads_db."""

    def __init__(self) -> None:
        self._records: dict[str, SourceRecord] = {}

    def register(self, record: SourceRecord) -> None:
        record.validate()
        source_id = record.contract.source_id
        if source_id in self._records:
            raise ValueError(f"source already registered: {source_id}")
        self._records[source_id] = record

    def get(self, source_id: str) -> SourceRecord:
        try:
            return self._records[source_id]
        except KeyError as exc:
            raise KeyError(f"unknown source: {source_id}") from exc

    def list(self) -> tuple[SourceRecord, ...]:
        return tuple(self._records[key] for key in sorted(self._records))

    def activate(self, source_id: str) -> SourceRecord:
        current = self.get(source_id)
        if current.lifecycle in (SourceLifecycle.RETIRED, SourceLifecycle.SUSPENDED):
            raise ValueError(f"source cannot be activated from {current.lifecycle.value}")
        if not current.contract.legal_reviewed:
            raise ValueError("source cannot be activated before legal/provider review")
        if not current.contract.enabled:
            raise ValueError("source contract must be enabled before activation")
        return self._replace(current, lifecycle=SourceLifecycle.ACTIVE)

    def suspend(self, source_id: str) -> SourceRecord:
        current = self.get(source_id)
        if current.lifecycle is SourceLifecycle.RETIRED:
            raise ValueError("retired source cannot be suspended")
        return self._replace(current, lifecycle=SourceLifecycle.SUSPENDED)

    def retire(self, source_id: str) -> SourceRecord:
        current = self.get(source_id)
        disabled = replace(current.contract, enabled=False)
        return self._replace(current, contract=disabled, lifecycle=SourceLifecycle.RETIRED)

    def record_success(self, source_id: str, at: datetime | None = None) -> SourceRecord:
        current = self.get(source_id)
        timestamp = self._timestamp(at)
        return self._replace(
            current,
            health=SourceHealth.HEALTHY,
            last_success_at=timestamp,
        )

    def record_failure(self, source_id: str, at: datetime | None = None) -> SourceRecord:
        current = self.get(source_id)
        timestamp = self._timestamp(at)
        return self._replace(
            current,
            health=SourceHealth.FAILED,
            last_failure_at=timestamp,
        )

    def ingestion_allowed(self, source_id: str) -> bool:
        record = self.get(source_id)
        return record.lifecycle is SourceLifecycle.ACTIVE and record.contract.enabled

    def _replace(self, current: SourceRecord, **changes: Any) -> SourceRecord:
        updated = replace(current, **changes)
        updated.validate()
        self._records[current.contract.source_id] = updated
        return updated

    @staticmethod
    def _timestamp(value: datetime | None) -> datetime:
        timestamp = value or datetime.now(UTC)
        if timestamp.tzinfo is None:
            raise ValueError("source health timestamp must be timezone-aware")
        return timestamp
