from datetime import UTC, datetime

import pytest

from tads_contracts import (
    CanonicalEventRef,
    EvidenceRef,
    ObservationRef,
    ProvenanceRef,
    SignalRef,
)


def evidence() -> EvidenceRef:
    return EvidenceRef(
        "ev-1",
        ProvenanceRef("src-1", "snap-1", "sha256:abc", datetime.now(UTC), "test", "1"),
        0.9,
    )


def test_observation_is_distinct_from_signal() -> None:
    observation = ObservationRef("obs-1", "src-1", "snap-1", datetime.now(UTC), "sha256:abc")
    observation.validate()
    assert not isinstance(observation, SignalRef)


def test_event_requires_observation_lineage() -> None:
    event = CanonicalEventRef("evt-1", "job_posted", ("obs-1",), None)
    event.validate()


def test_signal_requires_event_and_evidence() -> None:
    signal = SignalRef("sig-1", "acct-1", "hiring", "evt-1", (evidence(),), 0.8)
    signal.validate()


def test_signal_without_evidence_is_invalid() -> None:
    signal = SignalRef("sig-1", "acct-1", "hiring", "evt-1", (), 0.8)
    with pytest.raises(ValueError, match="evidence"):
        signal.validate()
