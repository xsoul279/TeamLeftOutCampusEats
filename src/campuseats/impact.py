"""US9: Vendor impact totals for listings posted within a date range."""

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo
from flask import Blueprint, abort, flash, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import case, func, select

from .extensions import db
from .models import Listing, Reservation, ReservationStatus
from .pickups import mark_no_shows

impact_bp = Blueprint("impact", __name__)

def _date_bounds(start_text, end_text):
    """Include the start and end dates."""
    try:
        start = date.fromisoformat(start_text)
        end = date.fromisoformat(end_text)
    except ValueError:
        raise ValueError("Enter valid start and end dates.") from None

    if start > end:
        raise ValueError("Start date must be on or before end date.")

    try: 
        after_end = end + timedelta(days=1)
    except OverflowError:
        raise ValueError("End date must be before 9999-12-31.") from None

    return (
        datetime.combine(start, time.min),
        datetime.combine(after_end, time.min),
    )

@impact_bp.get("/impact")
@login_required
def dashboard():
    if current_user.role != "vendor":
        abort(
            403,
            description="Only vendors can view the impact dashboard.",
        )

    today = datetime.now(ZoneInfo("America/Denver")).date()

    start_text = request.args.get(
        "start_date",
        today.replace(day=1).isoformat(),
    )
    end_text = request.args.get("end_date", today.isoformat())

    def show_dashboard(metrics, status=200):
        return render_template(
            "impact_dashboard.html",
            metrics=metrics,
            start_date=start_text,
            end_date=end_text,
        ), status

    try:
        start, after_end = _date_bounds(start_text, end_text)
    except ValueError as error:
        flash(str(error), "error")
        return show_dashboard(None, 400)

    # Update expired reservations before calculating totals.
    mark_no_shows(current_user.id)
    db.session.commit()

    listing_filters = (
        Listing.vendor_id == current_user.id,
        Listing.created_at >= start,
        Listing.created_at < after_end,
    )

    # Count listings separately so reservations do not duplicate totals.
    listings_posted, portions_posted = db.session.execute(
        select(
            func.count(Listing.id),
            func.coalesce(func.sum(Listing.portions), 0),
        ).where(*listing_filters)
    ).one()

    picked_up, no_show_count, no_show_portions, reserved = (
        db.session.execute(
            select(
                func.coalesce(
                    func.sum(
                        case(
                            (
                                Reservation.status
                                == ReservationStatus.PICKED_UP,
                                Reservation.portions,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ),
                func.count(
                    case(
                        (
                            Reservation.status
                            == ReservationStatus.NO_SHOW,
                            1,
                        )
                    )
                ),
                func.coalesce(
                    func.sum(
                        case(
                            (
                                Reservation.status
                                == ReservationStatus.NO_SHOW,
                                Reservation.portions,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ),
                func.coalesce(
                    func.sum(
                        case(
                            (
                                Reservation.status.in_(
                                    (
                                        ReservationStatus.ACTIVE,
                                        ReservationStatus.PICKED_UP,
                                        ReservationStatus.NO_SHOW,
                                    )
                                ),
                                Reservation.portions,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ),
            )
            .select_from(Reservation)
            .join(Listing, Reservation.listing_id == Listing.id)
            .where(*listing_filters)
        ).one()
    )

    return show_dashboard(
        {
            "listings_posted": listings_posted,
            "portions_posted": portions_posted,
            "portions_picked_up": picked_up,
            "no_show_count": no_show_count,
            "no_show_portions": no_show_portions,
            "portions_reserved": reserved,
            "no_show_rate": (
                no_show_portions / reserved * 100 if reserved else 0
            ),
        }
    )