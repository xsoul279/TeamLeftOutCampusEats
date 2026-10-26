"""CampusEats application factory."""

import os
from collections.abc import Mapping
from typing import Any

from flask import Flask

from .config import database_url
from .extensions import db


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

    # Plain `flask run` has no database, so only connect when one is configured.
    if app.config["SQLALCHEMY_DATABASE_URI"]:
        db.init_app(app)
    from . import models  # noqa: F401  (registers the tables with db)

    from .main import bp

    app.register_blueprint(bp)
    return app
