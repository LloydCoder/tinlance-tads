"""Run pending TADS database migrations."""

import os

from .migrate import apply_migrations

for name in apply_migrations(os.environ["DATABASE_URL"]):
    print(name)
