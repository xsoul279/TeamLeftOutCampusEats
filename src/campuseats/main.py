"""Public pages shared by students and vendors."""

from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.get("/")
def index() -> str:
    """Show the CampusEats home page."""
    return render_template("index.html")
