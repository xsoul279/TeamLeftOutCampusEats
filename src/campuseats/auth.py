from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from .extensions import db
from .models import User

auth_bp = Blueprint("auth", __name__, template_folder="templates")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.home"))


    if request.method == "POST":
        name = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "")
        
        errors = []
    
        if not name:
            errors.append("Username is required.")
        elif len(name) > 100:
            errors.append("Username should be 100 characters or less.")
        if not email:
            errors.append("Email is required.")
        if not password:
            errors.append("Password is required.")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if role not in ["student", "vendor"]:
            errors.append("Must select a valid role: 'student', 'vendor'.")

        if not errors and User.query.filter_by(email=email).first():
            errors.append("Email is already registered.")
        if not errors and User.query.filter_by(username=name).first():
            errors.append("Username is already taken.")
        
        if errors:
            for error in errors:
                flash(error, "warning")
            return render_template("register.html", username=name, email=email, role=role), 400


        new_user = User(username=name, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("That email or username is already registered.", "warning")
            return render_template("register.html", username=name, email=email, role=role), 400
        flash("Account creation successful! Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = User.query.filter_by(email=email).first()
        password = request.form.get("password", "")
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("auth.home"))
        flash("Invalid email/password.", "warning")
        return render_template("login.html", email=email), 401
    return render_template("login.html")


@auth_bp.route("/home")
@login_required
def home():
    page = "vendor_home.html" if current_user.role == "vendor" else "student_home.html"
    return render_template(page)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
