"""Fail-closed HTTP adapter for a verified ReconOS capability contract.

This adapter is intentionally provider-specific at the boundary but provider-neutral
inside TADS. It refuses non-HTTPS endpoints, arbitrary hosts, redirects, oversized
responses, malformed JSON, request-id mismatches and evidence-free results.

Network-layer egress controls remain mandatory in production; application validation
cannot by itself eliminate DNS/network race conditions.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import IO, Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .models import EnrichmentRequest, EnrichmentResult


class ReconOSAdapterError(RuntimeError):
    """Raised when the ReconOS boundary cannot safely produce a validated result."""


class _RejectRedirects(HTTPRedirectHandler):
    def redirect_request(
        self,
        req: Request,
        fp: IO[bytes],
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> Request | None:
        raise ReconOSAdapterError("ReconOS redirects are forbidden")


@dataclass(frozen=True, slots=True)
class ReconOSHttpAdapter:
    """Authenticated adapter for the documented TADS↔ReconOS HTTP contract."""

    endpoint: str
    bearer_token: str
    allowed_host: str
    max_response_bytes: int = 1_048_576

    def __post_init__(self) -> None:
        parsed = urlparse(self.endpoint)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("ReconOS endpoint must use HTTPS with a hostname")
        if parsed.username or parsed.password:
            raise ValueError("ReconOS endpoint must not contain URL userinfo")
        if parsed.port not in (None, 443):
            raise ValueError("ReconOS endpoint must use the standard HTTPS port")
        if parsed.hostname != self.allowed_host:
            raise ValueError("ReconOS endpoint host must exactly match allowed_host")
        if not self.bearer_token.strip():
            raise ValueError("ReconOS bearer token is required")
        if not 0 < self.max_response_bytes <= 10 * 1024 * 1024:
            raise ValueError("max_response_bytes must be between 1 and 10485760")

    def enrich(self, request: EnrichmentRequest) -> EnrichmentResult:
        request_id = request.request_id or str(uuid.uuid4())
        payload = {
            "schema_version": request.schema_version,
            "request_id": request_id,
            "account_id": request.account_id,
            "purpose": request.purpose,
            "fields": list(request.fields),
            "evidence_required": request.evidence_required,
            "authorization_id": request.authorization_id,
            "audit_correlation_id": request.audit_correlation_id,
        }
        body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        http_request = Request(
            self.endpoint,
            data=body,
            method="POST",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json",
                "Idempotency-Key": request_id,
                "X-TADS-Schema-Version": request.schema_version,
            },
        )
        opener = build_opener(_RejectRedirects())
        try:
            with opener.open(http_request, timeout=request.timeout_seconds) as response:
                if response.status != 200:
                    raise ReconOSAdapterError(
                        f"ReconOS returned unexpected HTTP status {response.status}"
                    )
                content_length = response.headers.get("Content-Length")
                if content_length is not None and int(content_length) > self.max_response_bytes:
                    raise ReconOSAdapterError("ReconOS response exceeds configured byte budget")
                raw = response.read(self.max_response_bytes + 1)
        except HTTPError as exc:
            raise ReconOSAdapterError(
                f"ReconOS request failed with HTTP status {exc.code}"
            ) from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise ReconOSAdapterError("ReconOS request failed") from exc

        if len(raw) > self.max_response_bytes:
            raise ReconOSAdapterError("ReconOS response exceeds configured byte budget")
        try:
            document = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ReconOSAdapterError("ReconOS response is not valid JSON") from exc
        return self._parse_result(document, request_id)

    @staticmethod
    def _parse_result(document: object, request_id: str) -> EnrichmentResult:
        if not isinstance(document, dict):
            raise ReconOSAdapterError("ReconOS response must be a JSON object")

        def required_text(name: str) -> str:
            value = document.get(name)
            if not isinstance(value, str) or not value.strip():
                raise ReconOSAdapterError(f"ReconOS response field {name!r} is required")
            return value

        response_request_id = required_text("request_id")
        if response_request_id != request_id:
            raise ReconOSAdapterError("ReconOS response request_id does not match request")

        raw_evidence = document.get("evidence_ids")
        if not isinstance(raw_evidence, list) or not raw_evidence or not all(
            isinstance(value, str) and value.strip() for value in raw_evidence
        ):
            raise ReconOSAdapterError("ReconOS response requires non-empty evidence_ids")

        raw_facts = document.get("facts", [])
        if not isinstance(raw_facts, list):
            raise ReconOSAdapterError("ReconOS response facts must be an array")
        facts: list[tuple[str, str]] = []
        for fact in raw_facts:
            if (
                not isinstance(fact, dict)
                or not isinstance(fact.get("key"), str)
                or not isinstance(fact.get("value"), str)
            ):
                raise ReconOSAdapterError("ReconOS facts must contain string key/value objects")
            facts.append((fact["key"], fact["value"]))

        raw_unknowns = document.get("unknowns", [])
        if not isinstance(raw_unknowns, list) or not all(
            isinstance(value, str) and value.strip() for value in raw_unknowns
        ):
            raise ReconOSAdapterError("ReconOS unknowns must be an array of non-empty strings")

        received_at = datetime.now(UTC)
        return EnrichmentResult(
            provider=required_text("provider"),
            provider_version=required_text("provider_version"),
            account_id=required_text("account_id"),
            evidence_ids=tuple(raw_evidence),
            facts=tuple(facts),
            unknowns=tuple(raw_unknowns),
            response_id=required_text("response_id"),
            request_id=response_request_id,
            schema_version=required_text("schema_version"),
            received_at=received_at,
        )
