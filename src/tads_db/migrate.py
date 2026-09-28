"""Forward-only SQL migration runner."""
from pathlib import Path
import os
import psycopg
MIGRATIONS=Path(__file__).parents[2]/"database"/"migrations"
def apply_migrations(dsn:str)->list[str]:
    applied=[]
    with psycopg.connect(dsn) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations(version text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now())")
        existing={row[0] for row in conn.execute("SELECT version FROM schema_migrations ORDER BY version").fetchall()}
        files=sorted(p for p in MIGRATIONS.glob("*.sql"))
        unknown=existing-{p.name for p in files}
        if unknown: raise RuntimeError(f"unknown migration history: {sorted(unknown)}")
        for path in files:
            if path.name in existing: continue
            with conn.transaction():
                conn.execute(path.read_text(encoding="utf-8"))
                conn.execute("INSERT INTO schema_migrations(version) VALUES (%s)",(path.name,))
            applied.append(path.name)
    return applied
if __name__=="__main__":
    for name in apply_migrations(os.environ["DATABASE_URL"]): print(name)