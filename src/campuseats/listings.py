from datetime import datetime
from zoneinfo import ZoneInfo

from flask import (
    Blueprint, abort, flash, redirect, render_template, request, url_for,
)
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from .extensions import db
from .models import DietaryTag, Listing

listings_bp = Blueprint("listings", __name__)

@listings_bp.route("/listings/new", methods=["GET", "POST"])
@login_required
def new_listing():
    if current_user.role != "vendor":
        abort(403, description="You do not have permission to create a listing.")

    def show_form(status=200):
        return render_template("new_listing.html", dietary_tags=list(DietaryTag),), status

    if request.method == "GET":
        return show_form()

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    location = request.form.get("pickup_location", "").strip()
    errors = []

    if not title or len(title) >120:
        errors.append("Title is required and must be less than 120 characters.")
    if not description:
        errors.append("Description is required.")
    if not location or len(location) > 200:
        errors.append("Enter a valid pickup location of 1 to 200 characters")

    try:
        portions = int(request.form.get("portions", ""))
        if not 1 <= portions <= 100:
            raise ValueError
    except ValueError:
        errors.append("Portions must be a number between 1 and 100.")
    tags = []

    for tag_name in set(request.form.getlist("tags")):
        try:
            tags.append(DietaryTag[tag_name])
        except KeyError:
            errors.append(f"Invalid dietary tag: {tag_name}")

    try:
        start = datetime.fromisoformat(request.form.get("pickup_start", ""))
        end = datetime.fromisoformat(request.form.get("pickup_end", ""))

        if start.tzinfo is not None or end.tzinfo is not None:
            raise ValueError

        now = datetime.now(ZoneInfo("America/Denver")).replace(tzinfo=None)

        if end <= start:
             errors.append("Pickup end time must be after pickup start time.")
        if start < now:
            errors.append("Pickup start time must be in the future.")
        if end <= now:
            errors.append("Pickup end time must be in the future.")
    except ValueError:
        errors.append("Invalid pickup start or end time.")

    if errors:
        for error in errors:
            flash(error, "error")
        return show_form(400)

    listing = Listing(
        vendor_id=current_user.id,
        title=title,
        description=description,
        portions=portions,
        portions_remaining=portions,
        pickup_location=location,
        pickup_start=start,
        pickup_end=end,
        tags=tags,
    )
    db.session.add(listing)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash("An error occurred while creating the listing.", "error")
        return show_form(500)

    flash("Listing created successfully.", "success")
    return redirect(url_for("listings.new_listing"))
            