from datetime import UTC, datetime

import pytest

from tads_change import AccountStateSnapshot, ChangeDetector, ChangeKind


def snapshot(attributes: dict[str, object], minute: int) -> AccountStateSnapshot:
    return AccountStateSnapshot(
        account_id="acct-1",
        observed_at=datetime(2026, 10, 3, 11, minute, tzinfo=UTC),
        attributes=attributes,
        evidence_ids=("ev-1",),
    )


def test_first_snapshot_is_emergence() -> None:
    change = ChangeDetector.compare(None, snapshot({"hiring": True}, 0))
    assert change is not None
    assert change.kind is ChangeKind.EMERGENCE
    assert change.changed_fields == ("hiring",)


def test_material_change_is_deterministic() -> None:
    change = ChangeDetector.compare(
        snapshot({"hiring": False, "region": "EU"}, 0),
        snapshot({"hiring": True, "region": "US"}, 1),
    )
    assert change is not None
    assert change.kind is ChangeKind.MATERIAL_CHANGE
    assert change.changed_fields == ("hiring", "region")


def test_disappearance_is_distinguished() -> None:
    change = ChangeDetector.compare(
        snapshot({"funding": "active"}, 0),
        snapshot({}, 1),
    )
    assert change is not None
    assert change.kind is ChangeKind.DISAPPEARANCE


def test_identical_state_has_no_change() -> None:
    assert (
        ChangeDetector.compare(snapshot({"hiring": True}, 0), snapshot({"hiring": True}, 1)) is None
    )


def test_cross_account_comparison_is_rejected() -> None:
    first = snapshot({"hiring": True}, 0)
    second = AccountStateSnapshot("acct-2", first.observed_at, first.attributes, first.evidence_ids)
    with pytest.raises(ValueError, match="same account"):
        ChangeDetector.compare(first, second)
