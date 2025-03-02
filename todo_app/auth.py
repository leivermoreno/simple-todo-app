import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from db import db
from models import Task, User, Project


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if g.user:
        return redirect(url_for("index"))

    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]

        error = None

        if not email or not password or not name:
            error = "Email, password, and name are required."

        if not error:
            try:
                password = generate_password_hash(password)
                user = User(email=email, password=password, name=name)
                project = Project(name="My first project")
                user.projects.append(project)
                task = Task(text="First task")
                project.tasks.append(task)
                db.session.add(user)
                db.session.commit()
                flash("Registration successful! You can now log in.")

                return redirect(url_for("auth.login"))
            except IntegrityError:
                error = "Email is already registered."

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if g.user:
        return redirect(url_for("index"))

    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        error = None

        if not email or not password:
            error = "Email and password are required."

        if not error:
            stmt = select(User).where(User.email == email)
            user = db.session.scalar(stmt)
            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id
                return redirect(url_for("index"))

            error = "Incorrect email or password."

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        stmt = select(User).where(User.id == user_id)
        g.user = db.session.scalar(stmt)


@bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def login_required(view=None):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        if view is not None:
            return view(**kwargs)

    return wrapped
