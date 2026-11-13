from datetime import datetime
from zoneinfo import ZoneInfo
import secrets

from flask import (
    Blueprint, abort, flash, redirect, render_template, request, url_for,
)
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from .extensions import db
from .models import DietaryTag, Listing, Reservation, ReservationStatus

reservations_bp = Blueprint("reservations", __name__)

def _local_now():
    return datetime.now(ZoneInfo("America/Denver")).replace(tzinfo=None)


@reservations_bp.get("/reservations")
@login_required
def view_reservations():
    if current_user.role != "student":
        abort(403, description="Only students can view reservations.")

    now = _local_now()
    reservations = db.session.scalars(
        select(Reservation)
        .where(
            Reservation.student_id == current_user.id
        )
        .order_by(Reservation.pickup_end)
    ).all()

    return render_template("reservations.html", reservations=reservations, now=now)

@reservations_bp.post("/reservations/<int:reservation_id>/cancel")
@login_required
def cancel_reservation(reservation_id):
    if current_user.role != "student":
        abort(403, description="Only students can cancel reservations.")

    reservation = db.session.get(Reservation, reservation_id)
    if not reservation or reservation.student_id != current_user.id:
        abort(404, description="Reservation not found.")

    listing = db.session.get(Listing, reservation.listing_id)
    db.session.refresh(reservation, with_for_update=True)
    
    if reservation.pickup_end <= _local_now():
        db.session.rollback()
        flash("This reservation cannot be canceled.", "error")
        return redirect(url_for("reservations.view_reservations"))
    
    if reservation.status != ReservationStatus.ACTIVE:
        db.session.rollback()
        flash("This reservation cannot be canceled.", "error")
        return redirect(url_for("reservations.view_reservations"))

    reservation.status = ReservationStatus.CANCELED
    listing.portions_remaining += reservation.portions
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash("Something went wrong canceling this reservation. Please try again.", "error")
        return redirect(url_for("reservations.view_reservations"))

    flash("Reservation canceled successfully.", "success")
    return redirect(url_for("reservations.view_reservations"))