from datetime import UTC, datetime

import pytest

from tads_accounts import AccountIntelligenceEngine, AccountSignal


def test_empty_account_state_is_explicit() -> None:
    state = AccountIntelligenceEngine().derive("a1", [])
    assert state.active_signal_count == 0
    assert state.drivers == ("no active signals",)


def test_account_state_is_deterministic_and_explainable() -> None:
    now = datetime.now(UTC)
    signals = [
        AccountSignal("s1", "hiring", 0.8, 1.0, 1, now),
        AccountSignal("s2", "security", 0.6, 0.9, 1, now),
        AccountSignal("s3", "regulatory", 0.2, 0.5, -1, now),
    ]
    state = AccountIntelligenceEngine().derive("a1", signals, momentum=0.7)
    assert state.signal_strength == pytest.approx(0.533333)
    assert state.signal_diversity == 1.0
    assert state.negative_evidence == pytest.approx(1 / 3)
    assert state.data_confidence == pytest.approx(0.8)
    assert state.momentum == 0.7


def test_invalid_momentum_is_rejected() -> None:
    with pytest.raises(ValueError):
        AccountIntelligenceEngine().derive("a1", [], momentum=1.1)
