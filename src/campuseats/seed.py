"""Create demo datasets without changing existing application data."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import secrets
import string

import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy import DateTime, String, func, select
from sqlalchemy.orm import Mapped, mapped_column

from .extensions import db
from .models import DietaryTag, Listing, Reservation, ReservationStatus, User

SEED_NAME = "sprint-1-demo-v1"
EXTRA_SEED_NAME = "sprint-2-fixtures-v1"
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


def _seed_initial_data() -> None:
    """Create the original demo accounts and available listings."""
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


def _pickup_code() -> str:
    """Choose an unused six-character code for a fixture reservation."""
    alphabet = string.ascii_uppercase + string.digits
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(6))
        existing = db.session.scalar(
            select(Reservation.id).where(Reservation.pickup_code == code)
        )
        if existing is None:
            return code


def _seed_extra_data() -> None:
    """Add historical and availability fixtures without changing existing rows."""
    vendor = _account(
        "Flat Top Grill", "flattopgrill@msudenver.edu", "grilled_cheese8", "vendor"
    )
    student = _account("Lucky Guy", "identityv@msudenver.edu", "luckisAskill2", "student")
    second_vendor = _account(
        "Campus Cafe", "campuscafe@campuseats.example", "cafe_demo20", "vendor"
    )
    db.session.flush()
    now = datetime.now(ZoneInfo("America/Denver")).replace(tzinfo=None, microsecond=0)
    ended = Listing(
        vendor_id=vendor.id, title="[Demo] Ended vegetarian tray",
        description="An ended pickup window with one uncollected reservation.",
        portions=3, portions_remaining=2, pickup_location="Student Union counter",
        pickup_start=now - timedelta(hours=3), pickup_end=now - timedelta(hours=2),
        tags=[DietaryTag.VEGETARIAN],
    )
    cancelled = Listing(
        vendor_id=vendor.id, title="[Demo] Cancelled bakery bags",
        description="A cancelled listing with a cancelled reservation.",
        portions=4, portions_remaining=4, pickup_location="Bakery pickup desk",
        pickup_start=now + timedelta(hours=1), pickup_end=now + timedelta(hours=4),
        cancelled=True, tags=[DietaryTag.CONTAINS_NUTS],
    )
    sold_out = Listing(
        vendor_id=vendor.id, title="[Demo] Sold-out soup",
        description="Both portions are held by one active reservation.",
        portions=2, portions_remaining=0, pickup_location="Student Union counter",
        pickup_start=now - timedelta(minutes=15), pickup_end=now + timedelta(hours=4),
        tags=[DietaryTag.VEGAN, DietaryTag.GLUTEN_FREE],
    )
    other_vendor = Listing(
        vendor_id=second_vendor.id, title="[Demo] Campus Cafe sandwiches",
        description="An available listing owned by the second vendor.",
        portions=7, portions_remaining=7, pickup_location="Campus Cafe counter",
        pickup_start=now + timedelta(minutes=30), pickup_end=now + timedelta(hours=5),
        tags=[],
    )
    db.session.add_all([ended, cancelled, sold_out, other_vendor])
    db.session.flush()
    for listing, portions, status in (
        (ended, 1, ReservationStatus.ACTIVE),
        (cancelled, 1, ReservationStatus.CANCELLED),
        (sold_out, 2, ReservationStatus.ACTIVE),
    ):
        db.session.add(Reservation(
            student_id=student.id, listing_id=listing.id, portions=portions,
            pickup_code=_pickup_code(), status=status,
        ))


def seed_database() -> bool:
    """Apply each demo dataset once in a serialized PostgreSQL transaction."""
    changed = False
    with db.session.begin():
        db.session.execute(select(func.pg_advisory_xact_lock(SEED_LOCK_ID)))
        for name, initialize in (
            (SEED_NAME, _seed_initial_data),
            (EXTRA_SEED_NAME, _seed_extra_data),
        ):
            if db.session.get(SeedRun, name) is None:
                initialize()
                db.session.add(SeedRun(name=name))
                changed = True
    return changed


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
