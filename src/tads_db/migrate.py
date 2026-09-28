"""Forward-only SQL migration runner."""

import os
from pathlib import Path

import psycopg

MIGRATIONS = Path(__file__).parent / "migrations"


def apply_migrations(dsn: str) -> list[str]:
    applied: list[str] = []
    with psycopg.connect(dsn) as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS schema_migrations(
                version text PRIMARY KEY,
                applied_at timestamptz NOT NULL DEFAULT now()
            )"""
        )
        existing = {
            row[0]
            for row in connection.execute(
                "SELECT version FROM schema_migrations ORDER BY version"
            ).fetchall()
        }
        files = sorted(MIGRATIONS.glob("*.sql"))
        unknown = existing - {path.name for path in files}
        if unknown:
            raise RuntimeError(f"unknown migration history: {sorted(unknown)}")
        for path in files:
            if path.name in existing:
                continue
            with connection.transaction():
                connection.execute(path.read_text(encoding="utf-8"))
                connection.execute(
                    "INSERT INTO schema_migrations(version) VALUES (%s)", (path.name,)
                )
            applied.append(path.name)
    return applied


if __name__ == "__main__":
    for name in apply_migrations(os.environ["DATABASE_URL"]):
        print(name)
