"""Forward-only SQL migration runner with integrity and concurrency protection."""

import hashlib
import os
from pathlib import Path

import psycopg

MIGRATIONS = Path(__file__).parent / "migrations"
LOCK_KEY = 4_839_271_006_421


def apply_migrations(dsn: str) -> list[str]:
    applied: list[str] = []
    with psycopg.connect(dsn) as connection:
        with connection.transaction():
            connection.execute("SELECT pg_advisory_xact_lock(%s)", (LOCK_KEY,))
            connection.execute(
                """CREATE TABLE IF NOT EXISTS schema_migrations(
                    version text PRIMARY KEY,
                    checksum text NOT NULL,
                    applied_at timestamptz NOT NULL DEFAULT now()
                )"""
            )
        files = sorted(MIGRATIONS.glob("*.sql"))
        known = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
        with connection.transaction():
            rows = connection.execute(
                "SELECT version, checksum FROM schema_migrations ORDER BY version"
            ).fetchall()
            existing = {row[0]: row[1] for row in rows}
            unknown = set(existing) - set(known)
            if unknown:
                raise RuntimeError(f"unknown migration history: {sorted(unknown)}")
            for version, checksum in existing.items():
                if known[version] != checksum:
                    raise RuntimeError(f"migration checksum mismatch: {version}")
            for path in files:
                if path.name in existing:
                    continue
                with connection.transaction():
                    connection.execute(path.read_text(encoding="utf-8"))
                    connection.execute(
                        "INSERT INTO schema_migrations(version,checksum) VALUES (%s,%s)",
                        (path.name, known[path.name]),
                    )
                applied.append(path.name)
    return applied


if __name__ == "__main__":
    for name in apply_migrations(os.environ["DATABASE_URL"]):
        print(name)
