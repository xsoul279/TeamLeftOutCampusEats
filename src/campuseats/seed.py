"""Create the initial demo dataset without changing existing application data."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy import DateTime, String, func, select
from sqlalchemy.orm import Mapped, mapped_column

from .extensions import db
from .models import DietaryTag, Listing, User

SEED_NAME = "sprint-1-demo-v1"
SEED_LOCK_ID = 0x43414D505553


class SeedRun(db.Model):
    """Record a completed bootstrap dataset so edits survive later startups."""

    __tablename__ = "seed_runs"

    name: Mapped[str] = mapped_column(String(64), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


def _account(username: str, email: str, password: str, role: str) -> User:
    """Reuse an account by email, preserving its current password and fields."""
    user = db.session.scalar(select(User).where(User.email == email))
    if user is not None:
        if user.role != role:
            raise ValueError("A demo account email is already used by another role.")
        return user
    if db.session.scalar(select(User.id).where(User.username == username)) is not None:
        raise ValueError("A demo account name is already used by another email.")
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    return user


def seed_database() -> bool:
    """Apply the demo dataset once, in a serialized PostgreSQL transaction."""
    with db.session.begin():
        db.session.execute(select(func.pg_advisory_xact_lock(SEED_LOCK_ID)))
        if db.session.get(SeedRun, SEED_NAME) is not None:
            return False

        vendor = _account(
            "Flat Top Grill", "flattopgrill@msudenver.edu", "grilled_cheese8", "vendor"
        )
        _account("Lucky Guy", "identityv@msudenver.edu", "luckisAskill2", "student")
        db.session.flush()

        now = datetime.now(ZoneInfo("America/Denver")).replace(tzinfo=None, microsecond=0)
        samples = (
            ("Vegetarian grain bowls", "Roasted vegetables and rice.", 8,
             "Student Union counter", [DietaryTag.VEGETARIAN]),
            ("Vegan lentil soup", "Lentil and vegetable soup in takeaway cups.", 6,
             "Campus Cafe counter", [DietaryTag.VEGAN, DietaryTag.GLUTEN_FREE]),
            ("Bakery bags", "A selection of surplus pastries.", 5,
             "Bakery pickup desk", []),
        )
        for offset, (title, description, portions, location, tags) in enumerate(samples):
            existing = db.session.scalar(
                select(Listing.id).where(
                    Listing.vendor_id == vendor.id, Listing.title == title
                )
            )
            if existing is None:
                db.session.add(Listing(
                    vendor_id=vendor.id,
                    title=title,
                    description=description,
                    portions=portions,
                    portions_remaining=portions,
                    pickup_location=location,
                    pickup_start=now + timedelta(minutes=30 + offset * 15),
                    pickup_end=now + timedelta(hours=4 + offset),
                    tags=tags,
                ))
        db.session.add(SeedRun(name=SEED_NAME))
    return True


@click.command("seed")
@with_appcontext
def seed_command() -> None:
    """Initialize demo data after the schema has been created."""
    if not current_app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise click.ClickException("Configure PostgreSQL before initializing demo data.")
    try:
        created = seed_database()
    except ValueError as error:
        raise click.ClickException(str(error)) from error
    click.echo("Demo data initialized." if created else "Demo data already initialized.")
