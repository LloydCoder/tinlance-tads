from dataclasses import replace
from datetime import UTC, datetime

import pytest

from tads_buying import BuyingWindow, BuyingWindowState


def window() -> BuyingWindow:
    return BuyingWindow(
        window_id="window-1",
        account_id="acct-1",
        state=BuyingWindowState.EMERGING,
        opened_at=datetime(2026, 10, 3, 11, 0, tzinfo=UTC),
        expires_at=datetime(2026, 10, 10, 11, 0, tzinfo=UTC),
        evidence_ids=("ev-1", "ev-2"),
        trigger_ids=("signal-1", "change-1"),
    )


def test_buying_window_is_not_purchase_intent() -> None:
    item = window()
    item.validate()
    assert item.is_purchase_intent_claim is False


def test_window_can_progress_and_expire() -> None:
    item = window()
    active = item.transition(BuyingWindowState.ACTIVE, datetime(2026, 10, 4, 11, 0, tzinfo=UTC))
    assert active.state is BuyingWindowState.ACTIVE
    dormant = active.transition(BuyingWindowState.ACTIVE, datetime(2026, 10, 11, 11, 0, tzinfo=UTC))
    assert dormant.state is BuyingWindowState.DORMANT


def test_invalidated_is_terminal_in_this_primitive() -> None:
    invalidated = window().transition(
        BuyingWindowState.INVALIDATED, datetime(2026, 10, 4, 11, 0, tzinfo=UTC)
    )
    assert invalidated.state is BuyingWindowState.INVALIDATED


def test_invalid_purchase_intent_claim_is_rejected() -> None:
    with pytest.raises(ValueError, match="purchase intent"):
        replace(window(), is_purchase_intent_claim=True).validate()


def test_expiry_must_follow_opening() -> None:
    with pytest.raises(ValueError, match="expire after"):
        BuyingWindow(
            "window-1",
            "acct-1",
            BuyingWindowState.EMERGING,
            datetime(2026, 10, 4, tzinfo=UTC),
            datetime(2026, 10, 3, tzinfo=UTC),
            ("ev-1",),
            ("signal-1",),
        ).validate()
