"""Append-only signal lifecycle and deterministic drift primitives."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class SignalLifecycle(StrEnum):
    DETECTED = "detected"
    STRENGTHENED = "strengthened"
    WEAKENED = "weakened"
    CORROBORATED = "corroborated"
    CONTRADICTED = "contradicted"
    STALE = "stale"
    EXPIRED = "expired"
    REACTIVATED = "reactivated"


@dataclass(frozen=True, slots=True)
class SignalEvent:
    signal_id: str
    lifecycle: SignalLifecycle
    occurred_at: datetime
    evidence_ids: tuple[str, ...]

    def validate(self) -> None:
        if not self.signal_id:
            raise ValueError("signal_id is required")
        if self.occurred_at.tzinfo is None:
            raise ValueError("signal event timestamp must be timezone-aware")
        if not self.evidence_ids:
            raise ValueError("signal lifecycle event requires evidence")


class SignalRegistry:
    """Append-only in-memory lifecycle history; persistence remains tads_db-owned."""

    def __init__(self) -> None:
        self._events: dict[str, list[SignalEvent]] = {}

    def append(self, event: SignalEvent) -> None:
        event.validate()
        history = self._events.setdefault(event.signal_id, [])
        if history and event.occurred_at < history[-1].occurred_at:
            raise ValueError("signal lifecycle events must be chronological")
        history.append(event)

    def history(self, signal_id: str) -> tuple[SignalEvent, ...]:
        return tuple(self._events.get(signal_id, ()))


@dataclass(frozen=True, slots=True)
class SignalDrift:
    false_positive_rate: float
    false_negative_rate: float
    source_reliability_delta: float
    taxonomy_change_rate: float
    threshold: float = 0.2

    def validate(self) -> None:
        rates = (
            self.false_positive_rate,
            self.false_negative_rate,
            self.source_reliability_delta,
            self.taxonomy_change_rate,
            self.threshold,
        )
        if any(not 0.0 <= value <= 1.0 for value in rates):
            raise ValueError("signal drift metrics must be within [0, 1]")

    @property
    def detected(self) -> bool:
        self.validate()
        return max(
            self.false_positive_rate,
            self.false_negative_rate,
            self.source_reliability_delta,
            self.taxonomy_change_rate,
        ) >= self.threshold
