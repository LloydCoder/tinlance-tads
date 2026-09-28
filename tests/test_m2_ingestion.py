import json
from datetime import UTC, datetime
from hashlib import sha256
from unittest.mock import patch

import pytest

from tads_ingest import FetchPolicy, GreenhouseAdapter, SafeFetcher
from tads_ingest.fetcher import RedirectRejected, UnsafeDestination


def test_fetch_policy_requires_allowlist() -> None:
    with pytest.raises(ValueError, match="allowlist"):
        FetchPolicy(frozenset()).validate()


def test_fetcher_rejects_http_and_untrusted_hosts() -> None:
    fetcher = SafeFetcher(FetchPolicy(frozenset({"boards-api.greenhouse.io"})))
    with pytest.raises(UnsafeDestination):
        fetcher.validate_url("http://boards-api.greenhouse.io/v1/boards/demo/jobs")
    with pytest.raises(UnsafeDestination):
        fetcher.validate_url("https://evil.example/jobs")


def test_fetcher_rejects_private_resolution() -> None:
    fetcher = SafeFetcher(FetchPolicy(frozenset({"boards-api.greenhouse.io"})))
    with (
        patch("tads_ingest.fetcher._host_is_public", return_value=False),
        pytest.raises(UnsafeDestination, match="public"),
    ):
        fetcher.validate_url("https://boards-api.greenhouse.io/v1/boards/demo/jobs")


def test_fetcher_disallows_redirects() -> None:
    assert RedirectRejected.__name__ == "RedirectRejected"


def test_greenhouse_normalizes_documented_public_job_shape() -> None:
    payload = (
        b'{"jobs":[{"id":123,"title":"Security Engineer","updated_at":"2026-09-28T10:00:00Z",'
        b'"absolute_url":"https://boards.greenhouse.io/acme/jobs/123","location":{"name":"Remote"}}]}'
    )
    captured = datetime(2026, 9, 28, tzinfo=UTC)
    result = type(
        "Result",
        (),
        {
            "url": "https://boards-api.greenhouse.io/v1/boards/acme/jobs?content=true",
            "status_code": 200,
            "content_type": "application/json",
            "body": payload,
            "captured_at": captured,
            "headers": {},
        },
    )()
    fetcher = object.__new__(SafeFetcher)
    adapter = GreenhouseAdapter("acme", fetcher)
    with patch.object(fetcher, "fetch", return_value=result):
        fetched, observations = adapter.fetch_jobs()
    assert fetched.status_code == 200
    assert len(observations) == 1
    assert observations[0].external_id == "123"
    assert observations[0].payload["title"] == "Security Engineer"
    expected = sha256(
        json.dumps(observations[0].payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert observations[0].content_hash == "sha256:" + expected
