"""Fail-closed production runtime configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class ProductionConfig:
    database_url: str
    object_storage_endpoint: str
    telemetry_endpoint: str
    max_concurrency: int = 8

    @classmethod
    def from_env(cls) -> ProductionConfig:
        required = {
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "OBJECT_STORAGE_ENDPOINT": os.getenv("OBJECT_STORAGE_ENDPOINT"),
            "OTEL_EXPORTER_OTLP_ENDPOINT": os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError("missing production configuration: " + ", ".join(sorted(missing)))
        return cls(
            database_url=required["DATABASE_URL"] or "",
            object_storage_endpoint=required["OBJECT_STORAGE_ENDPOINT"] or "",
            telemetry_endpoint=required["OTEL_EXPORTER_OTLP_ENDPOINT"] or "",
        )

    def validate(self) -> None:
        if not self.database_url.startswith(("postgresql://", "postgres://")):
            raise ValueError("DATABASE_URL must use PostgreSQL")
        for endpoint, name in (
            (self.object_storage_endpoint, "object_storage_endpoint"),
            (self.telemetry_endpoint, "telemetry_endpoint"),
        ):
            parsed = urlparse(endpoint)
            if parsed.scheme != "https" or not parsed.hostname:
                raise ValueError(f"{name} must be an HTTPS endpoint")
        if not 1 <= self.max_concurrency <= 256:
            raise ValueError("max_concurrency must be between 1 and 256")
