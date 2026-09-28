from tads_signals import SignalDetector, SignalKind, SignalState


def test_hiring_observation_becomes_validated_hiring_signal() -> None:
    signals = SignalDetector().detect(
        "obs-1",
        {"provider": "greenhouse", "title": "Backend Engineer"},
    )
    assert signals[0].kind is SignalKind.HIRING
    assert signals[0].state is SignalState.VALIDATED
    assert signals[0].evidence_observation_id == "obs-1"


def test_security_signal_requires_observed_security_language() -> None:
    signals = SignalDetector().detect(
        "obs-2",
        {"provider": "greenhouse", "title": "DevSecOps Engineer"},
    )
    assert any(signal.kind is SignalKind.SECURITY for signal in signals)


def test_unknown_provider_produces_no_signal() -> None:
    assert SignalDetector().detect("obs-3", {"provider": "unknown", "title": "Engineer"}) == ()
