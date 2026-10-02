"""Fail-closed HTTP adapter for the verified TADS↔FadeReach handoff contract.

The adapter publishes intelligence only. It has no outreach verbs, no message
generation, no recipient mutation and no follow-up controls.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .models import OpportunityHandoff
from .reconos_http import ReconOSAdapterError


class _RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, *args: object, **kwargs: object) -> None:
        raise ReconOSAdapterError("FadeReach redirects are forbidden")


@dataclass(frozen=True, slots=True)
class FadeReachHttpAdapter:
    """Authenticated adapter for the documented TADS↔FadeReach HTTP contract."""

    endpoint: str
    bearer_token: str
    allowed_host: str
    max_response_bytes: int = 262_144

    def __post_init__(self) -> None:
        parsed = urlparse(self.endpoint)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("FadeReach endpoint must use HTTPS with a hostname")
        if parsed.username or parsed.password:
            raise ValueError("FadeReach endpoint must not contain URL userinfo")
        if parsed.port not in (None, 443):
            raise ValueError("FadeReach endpoint must use the standard HTTPS port")
        if parsed.hostname != self.allowed_host:
            raise ValueError("FadeReach endpoint host must exactly match allowed_host")
        if not self.bearer_token.strip():
            raise ValueError("FadeReach bearer token is required")
        if not 0 < self.max_response_bytes <= 10 * 1024 * 1024:
            raise ValueError("max_response_bytes must be between 1 and 10485760")

    def publish(self, handoff: OpportunityHandoff) -> str:
        if handoff.expires_at is None:
            raise ReconOSAdapterError("FadeReach handoff requires an expiry")
        payload = {
            "schema_version": handoff.schema_version,
            "handoff_id": handoff.opportunity_id,
            "account_id": handoff.account_id,
            "score": handoff.score,
            "confidence": handoff.confidence,
            "hypothesis": handoff.hypothesis,
            "evidence_ids": list(handoff.evidence_ids),
            "recommended_persona": handoff.recommended_persona,
            "recommended_angle": handoff.recommended_angle,
            "timing": handoff.timing,
            "expires_at": handoff.expires_at.isoformat(),
            "audit_correlation_id": handoff.audit_correlation_id,
        }
        request = Request(
            self.endpoint,
            data=json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
            method="POST",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json",
                "Idempotency-Key": handoff.idempotency_key or "",
                "X-TADS-Schema-Version": handoff.schema_version,
            },
        )
        try:
            with build_opener(_RejectRedirects()).open(request, timeout=10) as response:
                if response.status not in (200, 201, 202):
                    raise ReconOSAdapterError(
                        f"FadeReach returned unexpected HTTP status {response.status}"
                    )
                content_length = response.headers.get("Content-Length")
                if content_length is not None and int(content_length) > self.max_response_bytes:
                    raise ReconOSAdapterError("FadeReach response exceeds configured byte budget")
                raw = response.read(self.max_response_bytes + 1)
        except HTTPError as exc:
            raise ReconOSAdapterError(
                f"FadeReach request failed with HTTP status {exc.code}"
            ) from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise ReconOSAdapterError("FadeReach request failed") from exc

        if len(raw) > self.max_response_bytes:
            raise ReconOSAdapterError("FadeReach response exceeds configured byte budget")
        try:
            document = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ReconOSAdapterError("FadeReach response is not valid JSON") from exc
        if not isinstance(document, dict):
            raise ReconOSAdapterError("FadeReach response must be a JSON object")
        response_schema = document.get("schema_version")
        response_id = document.get("handoff_id")
        if response_schema != handoff.schema_version:
            raise ReconOSAdapterError("FadeReach response schema_version does not match handoff")
        if not isinstance(response_id, str) or not response_id.strip():
            raise ReconOSAdapterError("FadeReach response requires a handoff_id")
        return response_id
