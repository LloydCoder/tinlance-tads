from __future__ import annotations

import json
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

import tads_integrations.fadereach_http as fadereach_http
from tads_integrations import FadeReachHttpAdapter, OpportunityHandoff, ReconOSAdapterError


class _FakeResponse:
    status = 202
    headers = {"Content-Length": "120"}

    def __init__(self, payload: dict[str, object]) -> None:
        self._raw = json.dumps(payload).encode()

    def read(self, limit: int) -> bytes:
        assert limit > len(self._raw)
        return self._raw

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, *args: object) -> None:
        return None


def _handoff() -> OpportunityHandoff:
    return OpportunityHandoff(
        "opp-1",
        "acct-1",
        0.8,
        0.7,
        "Evidence-backed attention hypothesis.",
        ("ev-1",),
        "security leader",
        "security engineering evidence",
        "now",
        datetime(2027, 1, 1, tzinfo=UTC),
        "handoff-1",
        audit_correlation_id="audit-1",
    )


def test_handoff_requires_future_timezone_aware_expiry() -> None:
    with pytest.raises(ValueError, match="expiry"):
        OpportunityHandoff(
            "opp-1",
            "acct-1",
            0.8,
            0.7,
            "hypothesis",
            ("ev-1",),
            None,
            None,
            "now",
            datetime(2026, 1, 1, tzinfo=UTC),
            "handoff-1",
        )


def test_adapter_requires_https_and_exact_host() -> None:
    with pytest.raises(ValueError):
        FadeReachHttpAdapter("http://reach.example/publish", "token", "reach.example")
    with pytest.raises(ValueError):
        FadeReachHttpAdapter("https://evil.example/publish", "token", "reach.example")


def test_adapter_publishes_idempotently_without_outreach_verbs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = {"schema_version": "tads.fadereach.v1", "handoff_id": "fr-1"}
    captured: dict[str, str] = {}

    class _Opener:
        def open(self, request: object, **_: object) -> _FakeResponse:
            headers = {key.lower(): value for key, value in request.header_items()}
            captured["authorization"] = headers.get("authorization", "")
            captured["idempotency"] = headers.get("idempotency-key", "")
            captured["schema"] = headers.get("x-tads-schema-version", "")
            body = json.loads(request.data.decode())
            assert body["evidence_ids"] == ["ev-1"]
            assert body["audit_correlation_id"] == "audit-1"
            assert "outreach" not in body
            assert "message" not in body
            return _FakeResponse(payload)

    monkeypatch.setattr(fadereach_http, "build_opener", lambda *_: _Opener())
    adapter = FadeReachHttpAdapter("https://reach.example/publish", "secret", "reach.example")
    assert adapter.publish(_handoff()) == "fr-1"
    assert captured == {
        "authorization": "Bearer secret",
        "idempotency": "handoff-1",
        "schema": "tads.fadereach.v1",
    }


def test_adapter_rejects_schema_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        fadereach_http,
        "build_opener",
        lambda *_: SimpleNamespace(
            open=lambda *_args, **_kwargs: _FakeResponse(
                {"schema_version": "wrong", "handoff_id": "fr-1"}
            )
        ),
    )
    adapter = FadeReachHttpAdapter("https://reach.example/publish", "secret", "reach.example")
    with pytest.raises(ReconOSAdapterError, match="schema_version"):
        adapter.publish(_handoff())
