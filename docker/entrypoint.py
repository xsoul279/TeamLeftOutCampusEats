"""Configure the container and wait for PostgreSQL before starting the server."""

import os
import secrets
import sys
import time

import psycopg

from campuseats import create_app
from campuseats.config import database_url
from campuseats.extensions import db
from campuseats.seed import seed_database


def configure_environment() -> str:
    """Build a connection URL and a per-container key when not supplied."""
    url = database_url()
    if url is None:
        raise SystemExit("Provide DATABASE_URL or the PostgreSQL settings.")
    os.environ["DATABASE_URL"] = url
    if not os.environ.get("SECRET_KEY"):
        os.environ["SECRET_KEY"] = secrets.token_hex(32)
    return os.environ["DATABASE_URL"].replace(
        "postgresql+psycopg://", "postgresql://", 1
    )


def wait_for_database(url: str) -> None:
    """Require a working database connection before launching the app."""
    deadline = time.monotonic() + 60
    while True:
        try:
            with psycopg.connect(url, connect_timeout=5, autocommit=True) as connection:
                connection.execute("SELECT 1")
            return
        except psycopg.OperationalError:
            if time.monotonic() >= deadline:
                raise SystemExit("PostgreSQL was not ready within 60 seconds.") from None
            print("Waiting for PostgreSQL...", file=sys.stderr, flush=True)
            time.sleep(2)


def initialize_database() -> None:
    """Create missing tables and seed data before the server workers start."""
    with create_app().app_context():
        db.create_all()
        seed_database()


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("A server command is required.")
    wait_for_database(configure_environment())
    initialize_database()
    os.execvp(sys.argv[1], sys.argv[1:])


if __name__ == "__main__":
    main()
