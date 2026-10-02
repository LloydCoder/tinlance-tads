from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

import tads_integrations.reconos_http as reconos_http
from tads_integrations import (
    EnrichmentRequest,
    ReconOSAdapterError,
    ReconOSHttpAdapter,
)


class _FakeResponse:
    status = 200
    headers = {"Content-Length": "300"}

    def __init__(self, payload: dict[str, object]) -> None:
        self._raw = json.dumps(payload).encode()

    def read(self, limit: int) -> bytes:
        assert limit > len(self._raw)
        return self._raw

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, *args: object) -> None:
        return None


def test_adapter_requires_https_and_exact_host() -> None:
    with pytest.raises(ValueError):
        ReconOSHttpAdapter("http://reconos.internal/enrich", "token", "reconos.internal")
    with pytest.raises(ValueError):
        ReconOSHttpAdapter("https://evil.example/enrich", "token", "reconos.internal")
    with pytest.raises(ValueError):
        ReconOSHttpAdapter("https://reconos.internal:8443/enrich", "token", "reconos.internal")


def test_adapter_rejects_mismatched_request_id(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = {
        "schema_version": "tads.reconos.v1",
        "request_id": "wrong",
        "response_id": "resp-1",
        "provider": "reconos",
        "provider_version": "2026-10",
        "account_id": "acct-1",
        "evidence_ids": ["ev-1"],
        "facts": [],
        "unknowns": [],
    }
    adapter = ReconOSHttpAdapter("https://reconos.example/enrich", "token", "reconos.example")
    monkeypatch.setattr(
        reconos_http,
        "build_opener",
        lambda *_: SimpleNamespace(open=lambda *_args, **_kwargs: _FakeResponse(payload)),
    )
    with pytest.raises(ReconOSAdapterError, match="request_id"):
        adapter.enrich(
            EnrichmentRequest(
                "acct-1",
                "validate technology need",
                ("technology",),
                request_id="req-1",
            )
        )


def test_adapter_sends_auth_idempotency_and_returns_validated_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = {
        "schema_version": "tads.reconos.v1",
        "request_id": "req-1",
        "response_id": "resp-1",
        "provider": "reconos",
        "provider_version": "2026-10",
        "account_id": "acct-1",
        "evidence_ids": ["ev-1"],
        "facts": [{"key": "technology", "value": "postgres"}],
        "unknowns": ["ownership"],
    }
    captured: dict[str, str] = {}

    class _Opener:
        def open(self, request: object, **_: object) -> _FakeResponse:
            captured["authorization"] = request.headers["Authorization"]
            captured["idempotency"] = request.headers["Idempotency-Key"]
            captured["schema"] = request.headers["X-tads-schema-version"]
            return _FakeResponse(payload)

    monkeypatch.setattr(reconos_http, "build_opener", lambda *_: _Opener())
    adapter = ReconOSHttpAdapter("https://reconos.example/enrich", "secret", "reconos.example")
    result = adapter.enrich(
        EnrichmentRequest(
            "acct-1",
            "validate technology need",
            ("technology",),
            request_id="req-1",
            authorization_id="auth-1",
            audit_correlation_id="audit-1",
        )
    )
    assert captured == {
        "authorization": "Bearer secret",
        "idempotency": "req-1",
        "schema": "tads.reconos.v1",
    }
    assert result.account_id == "acct-1"
    assert result.evidence_ids == ("ev-1",)
    assert result.facts == (("technology", "postgres"),)


def test_adapter_rejects_evidence_free_result() -> None:
    with pytest.raises(ReconOSAdapterError):
        ReconOSHttpAdapter._parse_result(
            {
                "schema_version": "tads.reconos.v1",
                "request_id": "req-1",
                "response_id": "resp-1",
                "provider": "reconos",
                "provider_version": "2026-10",
                "account_id": "acct-1",
                "evidence_ids": [],
                "facts": [],
                "unknowns": [],
            },
            "req-1",
        )
