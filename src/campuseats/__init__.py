"""CampusEats application factory."""

import os
from collections.abc import Mapping
from typing import Any

from flask import Flask

from .config import database_url
from .extensions import db, login_manager
from . import models  # noqa: F401  (registers the tables with db)
from .main import bp
from .auth import auth_bp
from .listings import listings_bp

   


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

    login_manager.init_app(app)
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(listings_bp)

    # Plain `flask run` has no database, so only connect when one is configured.
    if app.config["SQLALCHEMY_DATABASE_URI"]:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            from .seed import seed_database
            
            seed_database()
        


            
    return app