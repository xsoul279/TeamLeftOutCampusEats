"""Database configuration shared by the server and management commands."""

import os
from urllib.parse import quote


def database_url() -> str | None:
    """Resolve a PostgreSQL URL using the installed psycopg driver."""
    value = os.environ.get("DATABASE_URL")
    if value:
        for prefix in ("postgresql://", "postgres://"):
            if value.startswith(prefix):
                return value.replace(prefix, "postgresql+psycopg://", 1)
        if value.startswith("postgresql+psycopg://"):
            return value
        raise ValueError("DATABASE_URL must be a PostgreSQL URL using psycopg.")

    user = os.environ.get("POSTGRES_USER", "")
    password = os.environ.get("POSTGRES_PASSWORD", "")
    database = os.environ.get("POSTGRES_DB", "")
    if not all((user, password, database)):
        return None
    return (
        f"postgresql+psycopg://{quote(user, safe='')}:{quote(password, safe='')}"
        f"@db:5432/{quote(database, safe='')}"
    )
