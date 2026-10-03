"""Deterministic, evidence-backed account state change detection."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any


class ChangeKind(StrEnum):
    EMERGENCE = "emergence"
    MATERIAL_CHANGE = "material_change"
    ACCELERATION = "acceleration"
    DECELERATION = "deceleration"
    REVERSAL = "reversal"
    DISAPPEARANCE = "disappearance"


@dataclass(frozen=True, slots=True)
class AccountStateSnapshot:
    account_id: str
    observed_at: datetime
    attributes: dict[str, Any]
    evidence_ids: tuple[str, ...]

    def validate(self) -> None:
        if not self.account_id:
            raise ValueError("account_id is required")
        if self.observed_at.tzinfo is None:
            raise ValueError("account state timestamp must be timezone-aware")
        if not self.evidence_ids:
            raise ValueError("account state requires evidence")


@dataclass(frozen=True, slots=True)
class StateChange:
    account_id: str
    kind: ChangeKind
    changed_fields: tuple[str, ...]
    previous_observed_at: datetime | None
    observed_at: datetime
    evidence_ids: tuple[str, ...]

    def validate(self) -> None:
        if not self.changed_fields:
            raise ValueError("state change requires changed fields")
        if not self.evidence_ids:
            raise ValueError("state change requires evidence")
        if self.observed_at.tzinfo is None:
            raise ValueError("state change timestamp must be timezone-aware")
        if self.previous_observed_at is not None and self.observed_at < self.previous_observed_at:
            raise ValueError("state change timestamps must be chronological")


class ChangeDetector:
    @staticmethod
    def compare(
        previous: AccountStateSnapshot | None,
        current: AccountStateSnapshot,
    ) -> StateChange | None:
        current.validate()
        if previous is None:
            return StateChange(
                current.account_id,
                ChangeKind.EMERGENCE,
                tuple(sorted(current.attributes)),
                None,
                current.observed_at,
                current.evidence_ids,
            )

        previous.validate()
        if previous.account_id != current.account_id:
            raise ValueError("state snapshots must belong to the same account")
        if current.observed_at < previous.observed_at:
            raise ValueError("state snapshots must be chronological")

        fields = tuple(
            sorted(
                key
                for key in set(previous.attributes) | set(current.attributes)
                if previous.attributes.get(key) != current.attributes.get(key)
            )
        )
        if not fields:
            return None

        kind = ChangeKind.DISAPPEARANCE if all(
            key not in current.attributes for key in fields
        ) else ChangeKind.MATERIAL_CHANGE
        return StateChange(
            current.account_id,
            kind,
            fields,
            previous.observed_at,
            current.observed_at,
            current.evidence_ids,
        )
