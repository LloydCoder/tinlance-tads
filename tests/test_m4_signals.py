from tads_signals import SignalDetector, SignalKind, SignalState


def test_hiring_observation_becomes_validated_hiring_signal() -> None:
    signals = SignalDetector().detect(
        "obs-1",
        {"provider": "greenhouse", "title": "Backend Engineer"},
        ("ev-1",),
    )
    assert signals[0].kind is SignalKind.HIRING
    assert signals[0].state is SignalState.VALIDATED
    assert signals[0].evidence_observation_id == "obs-1"
    assert signals[0].evidence_ids == ("ev-1",)


def test_security_signal_requires_observed_security_language() -> None:
    signals = SignalDetector().detect(
        "obs-2",
        {"provider": "greenhouse", "title": "DevSecOps Engineer"},
        ("ev-2",),
    )
    assert any(signal.kind is SignalKind.SECURITY for signal in signals)


def test_unknown_provider_produces_no_signal() -> None:
    assert (
        SignalDetector().detect(
            "obs-3", {"provider": "unknown", "title": "Engineer"}, ("ev-3",)
        )
        == ()
    )


def test_signal_detection_requires_evidence() -> None:
    try:
        SignalDetector().detect(
            "obs-4", {"provider": "greenhouse", "title": "Engineer"}, ()
        )
    except ValueError as exc:
        assert "evidence" in str(exc)
    else:
        raise AssertionError("missing evidence must be rejected")
