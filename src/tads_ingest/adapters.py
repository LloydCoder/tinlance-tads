"""Provider adapters for documented hiring sources."""

import json
from dataclasses import dataclass
from hashlib import sha256
from typing import Any
from urllib.parse import quote

from .fetcher import SafeFetcher
from .models import FetchResult, NormalizedObservation

def _record_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + sha256(canonical).hexdigest()

@dataclass(frozen=True, slots=True)
class GreenhouseAdapter:
    board_token: str
    fetcher: SafeFetcher

    def fetch_jobs(self) -> tuple[FetchResult, tuple[NormalizedObservation, ...]]:
        token = quote(self.board_token, safe="")
        url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"
        result = self.fetcher.fetch(url)
        document = json.loads(result.body)
        observations = tuple(self._normalize(job, result) for job in document.get("jobs", []))
        return result, observations

    @staticmethod
    def _normalize(job: dict[str, Any], result: FetchResult) -> NormalizedObservation:
        external_id = str(job["id"])
        payload = {
            "provider": "greenhouse", "job_id": external_id,
            "internal_job_id": job.get("internal_job_id"), "title": job.get("title"),
            "updated_at": job.get("updated_at"), "first_published": job.get("first_published"),
            "company_name": job.get("company_name"), "location": job.get("location"),
            "absolute_url": job.get("absolute_url"), "content": job.get("content"),
            "departments": job.get("departments"), "offices": job.get("offices"),
        }
        return NormalizedObservation(
            external_id, "greenhouse_job_board", result.url, result.captured_at, payload, _record_hash(payload)
        )

@dataclass(frozen=True, slots=True)
class LeverAdapter:
    """Authenticated Lever adapter; no anonymous-access assumption is made."""

    account_id: str
    fetcher: SafeFetcher
    authorization_header: str

    def fetch_postings(self) -> tuple[FetchResult, tuple[NormalizedObservation, ...]]:
        if not self.account_id:
            raise ValueError("Lever account_id is required")
        if not self.authorization_header.startswith("Bearer "):
            raise ValueError("Lever authorization must be a Bearer token")
        url = "https://api.lever.co/v1/postings?state=published&distributionChannel=public&limit=100"
        result = self.fetcher.fetch(url, {"Authorization": self.authorization_header})
        document = json.loads(result.body)
        observations = tuple(self._normalize(posting, result) for posting in document.get("data", []))
        return result, observations

    @staticmethod
    def _normalize(posting: dict[str, Any], result: FetchResult) -> NormalizedObservation:
        external_id = str(posting["id"])
        payload = {
            "provider": "lever", "posting_id": external_id, "text": posting.get("text"),
            "created_at": posting.get("createdAt"), "updated_at": posting.get("updatedAt"),
            "categories": posting.get("categories"), "description_plain": posting.get("descriptionPlain"),
            "hosted_url": posting.get("hostedUrl"), "apply_url": posting.get("applyUrl"),
        }
        return NormalizedObservation(
            external_id, "lever_postings", result.url, result.captured_at, payload, _record_hash(payload)
        )
