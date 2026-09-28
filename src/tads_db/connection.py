"""Tenant-scoped PostgreSQL connection management."""
from contextlib import contextmanager
from typing import Iterator
import psycopg

class TenantConnection:
    def __init__(self, dsn: str, tenant_id: str):
        if not tenant_id:
            raise ValueError("tenant_id is required")
        self._dsn=dsn
        self.tenant_id=tenant_id
    @contextmanager
    def transaction(self) -> Iterator[psycopg.Connection]:
        with psycopg.connect(self._dsn) as conn:
            with conn.transaction():
                conn.execute("SELECT set_config('app.tenant_id', %s, true)", (self.tenant_id,))
                yield conn