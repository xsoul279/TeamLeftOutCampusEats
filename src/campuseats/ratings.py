"""US10: Students can rate their reservations."""

from flask import (
    Blueprint, abort, flash, redirect, render_template, request, url_for, )

from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .extensions import db
from .models import Rating, Reservation, ReservationStatus

ratings_bp = Blueprint("ratings", __name__)

def _rating_values(form):
    stars_text = form.get("stars", "")
    comment = form.get("comment", "").strip()
    errors = []

    if stars_text not in {"1", "2", "3", "4", "5"}:
        errors.append("Ratings must be from 1-5")

    if len(comment) > 300:
        errors.append("Comments must be 300 characters or less")

    return int(stars_text) if not errors else None, comment, errors

@ratings_bp.route( "/reservations/<int:reservation_id>/rate", methods=["GET", "POST"],)
@login_required
def rate_pickup(reservation_id):
    if current_user.role!="student":
        abort(403, description="Only students can rate reservations.")

    reservation = db.session.get(Reservation, reservation_id)
    if reservation is None or reservation.student_id != current_user.id:
        abort(404, description="Reservation not found.")

    def back_to_reservations(message):
        db.session.rollback()
        flash(message, "error")
        return redirect(url_for("reservations.view_reservations"))

    if reservation.status != ReservationStatus.PICKED_UP:
        return back_to_reservations("Only picked up reservations can be rated.")

    if reservation.rating is not None:
        return back_to_reservations("This reservation has already been rated.")

    def show_form(status=200):
        return render_template(
            "rate_pickup.html",
            reservation=reservation,), status
    if request.method == "GET":
        return show_form()
    stars, comment, errors = _rating_values(request.form)

    if errors:
        db.session.rollback()
        for error in errors:
            flash(error, "error")
        return show_form(400)

    db.session.add(Rating(
        reservation_id=reservation.id,
        stars=stars,
        comment=comment,
    ))

    try:
        db.session.commit()
    except IntegrityError:
        return back_to_reservations("This reservation has already been rated.")
    except SQLAlchemyError:
        db.session.rollback()
        flash("Something went wrong saving your rating. Please try again.", "error")
        return show_form(500)

    flash("Rating submitted successfully.", "success")
    return redirect(url_for("reservations.view_reservations"))
        
        
