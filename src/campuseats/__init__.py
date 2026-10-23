"""CampusEats application factory."""

import os
from collections.abc import Mapping
from typing import Any

from flask import Flask

from .config import database_url


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    """Create an application with environment-based configuration."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=database_url(),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    if test_config is not None:
        app.config.update(test_config)

    from .main import bp

    app.register_blueprint(bp)
    return app
