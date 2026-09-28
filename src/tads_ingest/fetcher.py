"""Hardened HTTP fetch boundary; arbitrary crawling is intentionally unsupported."""

from dataclasses import dataclass
from datetime import UTC, datetime
from ipaddress import ip_address
from socket import getaddrinfo
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .models import FetchResult


class FetchError(RuntimeError):
    """Controlled fetch failure."""


class RedirectRejected(FetchError):
    """Redirects are rejected unless a source policy explicitly permits them."""


class UnsafeDestination(FetchError):
    """Destination is not an allowed public network endpoint."""


@dataclass(frozen=True, slots=True)
class FetchPolicy:
    allowed_hosts: frozenset[str]
    timeout_seconds: float = 10.0
    max_bytes: int = 2_000_000
    allowed_content_types: frozenset[str] = frozenset(
        {"application/json", "application/ld+json", "text/plain", "text/html"}
    )
    allow_redirects: bool = False

    def validate(self) -> None:
        if not self.allowed_hosts:
            raise ValueError("fetch policy requires an explicit host allowlist")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.max_bytes <= 0:
            raise ValueError("max_bytes must be positive")
        if self.allow_redirects:
            raise ValueError("redirects require source-specific revalidation")


class _RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, *args: object, **kwargs: object) -> None:
        raise RedirectRejected("redirects are disabled by TADS source policy")


def _host_is_public(host: str) -> bool:
    try:
        addresses = {item[4][0] for item in getaddrinfo(host, None)}
    except OSError as exc:
        raise UnsafeDestination("destination DNS resolution failed") from exc
    if not addresses:
        raise UnsafeDestination("destination has no address")
    return all(ip_address(address).is_global for address in addresses)


class SafeFetcher:
    def __init__(self, policy: FetchPolicy):
        policy.validate()
        self.policy = policy
        self._opener = build_opener(_RejectRedirects)

    def validate_url(self, url: str) -> None:
        parts = urlsplit(url)
        if parts.scheme != "https":
            raise UnsafeDestination("only HTTPS sources are permitted")
        if parts.username or parts.password:
            raise UnsafeDestination("URL userinfo is not permitted")
        if parts.port not in (None, 443):
            raise UnsafeDestination("non-standard ports are not permitted")
        host = parts.hostname
        if not host or host.lower() not in self.policy.allowed_hosts:
            raise UnsafeDestination("destination host is not allowlisted")
        if not _host_is_public(host):
            raise UnsafeDestination("destination must resolve only to public addresses")

    def fetch(self, url: str, extra_headers: dict[str, str] | None = None) -> FetchResult:
        self.validate_url(url)
        headers = {
            "Accept": "application/json, text/html;q=0.8, text/plain;q=0.5",
            "User-Agent": "Tinlance-TADS/0.1 (+source-policy)",
        }
        if extra_headers:
            headers.update(extra_headers)
        request = Request(url, headers=headers, method="GET")
        captured_at = datetime.now(UTC)
        try:
            with self._opener.open(request, timeout=self.policy.timeout_seconds) as response:
                status = int(response.status)
                content_type = response.headers.get_content_type().lower()
                if content_type not in self.policy.allowed_content_types:
                    raise FetchError(f"unsupported content type: {content_type}")
                body = response.read(self.policy.max_bytes + 1)
                if len(body) > self.policy.max_bytes:
                    raise FetchError("response exceeded configured byte budget")
                headers = {
                    key.lower(): value
                    for key, value in response.headers.items()
                    if key.lower() in {"content-type", "etag", "last-modified", "cache-control"}
                }
                return FetchResult(url, status, content_type, body, captured_at, headers)
        except (HTTPError, URLError, TimeoutError) as exc:
            raise FetchError("source request failed") from exc
