"""Tenant-scoped PostgreSQL connection management."""

from contextlib import contextmanager
from typing import Any, Iterator

import psycopg
from psycopg import sql


class TenantConnection:
    def __init__(self, dsn: str, tenant_id: str, database_role: str | None = None):
        if not tenant_id:
            raise ValueError("tenant_id is required")
        self._dsn = dsn
        self.tenant_id = tenant_id
        self.database_role = database_role

    @contextmanager
    def transaction(self) -> Iterator[psycopg.Connection[Any]]:
        with psycopg.connect(self._dsn) as connection:
            with connection.transaction():
                if self.database_role:
                    connection.execute(
                        sql.SQL("SET LOCAL ROLE {}").format(sql.Identifier(self.database_role))
                    )
                connection.execute(
                    "SELECT set_config('app.tenant_id', %s, true)", (self.tenant_id,)
                )
                yield connection
