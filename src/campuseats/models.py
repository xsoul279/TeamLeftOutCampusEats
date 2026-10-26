"""Database models. Each class matches a class in uml/class.wsd."""

import enum
from datetime import datetime

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Index, String, Text, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db


class Role(enum.Enum):
    """Account type chosen at registration (US1)."""

    STUDENT = "Student"
    VENDOR = "Vendor"


class DietaryTag(enum.Enum):
    """Tags a vendor can put on a listing (US2)."""

    VEGETARIAN = "Vegetarian"
    VEGAN = "Vegan"
    GLUTEN_FREE = "Gluten-free"
    HALAL = "Halal"
    CONTAINS_NUTS = "Contains nuts"


class ReservationStatus(enum.Enum):
    """Where a reservation is in its life (US6, US7)."""

    ACTIVE = "Active"
    PICKED_UP = "Picked up"
    CANCELLED = "Cancelled"
    NO_SHOW = "No-show"


class User(db.Model):
    """A student or vendor account (US1)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum(Role, name="role"))
    creation_date: Mapped[datetime] = mapped_column(default=datetime.now)
    active: Mapped[bool] = mapped_column(default=True)

    listings: Mapped[list["Listing"]] = relationship(back_populates="vendor")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="student")


def _all_portions(context) -> int:
    """A new listing starts with every portion still available."""
    return context.get_current_parameters()["portions"]


class Listing(db.Model):
    """Surplus food posted by a vendor (US2)."""

    __tablename__ = "listings"
    __table_args__ = (
        CheckConstraint("portions BETWEEN 1 AND 100", name="listing_portions_range"),
        # US4 AC 4: remaining portions never go below zero.
        CheckConstraint(
            "portions_remaining BETWEEN 0 AND portions",
            name="listing_portions_remaining_range",
        ),
        CheckConstraint("pickup_end > pickup_start", name="listing_pickup_window_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    portions: Mapped[int]
    portions_remaining: Mapped[int] = mapped_column(default=_all_portions)
    pickup_location: Mapped[str] = mapped_column(String(120))
    pickup_start: Mapped[datetime]
    pickup_end: Mapped[datetime]
    cancelled: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    tags: Mapped[list[DietaryTag]] = mapped_column(
        ARRAY(Enum(DietaryTag, name="dietary_tag")), default=list
    )

    vendor: Mapped[User] = relationship(back_populates="listings")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="listing")

    @property
    def status(self) -> str:
        """Active, ended, or cancelled (US5). Calculated, not stored."""
        if self.cancelled:
            return "cancelled"
        if self.pickup_end <= datetime.now():
            return "ended"
        return "active"


class Reservation(db.Model):
    """Portions a student has reserved from a listing (US4)."""

    __tablename__ = "reservations"
    __table_args__ = (
        CheckConstraint("portions BETWEEN 1 AND 2", name="reservation_portions_range"),
        # US4 AC 3: a student holds at most one active reservation per listing.
        Index(
            "reservation_one_active_per_listing",
            "student_id",
            "listing_id",
            unique=True,
            postgresql_where=text("status = 'ACTIVE'"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"))
    portions: Mapped[int]
    pickup_code: Mapped[str] = mapped_column(String(6), unique=True)
    status: Mapped[ReservationStatus] = mapped_column(
        Enum(ReservationStatus, name="reservation_status"),
        default=ReservationStatus.ACTIVE,
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    student: Mapped[User] = relationship(back_populates="reservations")
    listing: Mapped[Listing] = relationship(back_populates="reservations")
