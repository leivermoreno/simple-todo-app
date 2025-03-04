from flask import (
    Blueprint,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import select

from auth import login_required
from db import db
from models import Project
from utils import get_project


bp = Blueprint("project", __name__)

bp.before_request(login_required())


@bp.get("/")
def index():
    return render_template("project/index.html", projects=g.user.projects)


@bp.get("/<int:project_id>")
def show_details(project_id):
    project = get_project(project_id)
    return render_template("project/details.html", project=project)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        name = request.form["name"]

        error = None

        if not name:
            error = "Name is required."

        if not error:
            project_id = request.form.get("project_id")
            if project_id is not None:
                project = get_project(project_id)
                project.name = name
            else:
                project = Project(name=name, user_id=g.user.id)
                db.session.add(project)

            db.session.commit()
            flash(
                f"Project {project.name} was {"updated" if project_id else "created"}."
            )
            return redirect(url_for("project.show_details", project_id=project.id))

        flash(error)

    project = None
    if request.method == "GET" and request.args.get("project_id") is not None:
        project = get_project(request.args.get("project_id"))

    return render_template("project/create.html", project=project)


@bp.get("/<int:project_id>/delete")
def delete(project_id):
    project = get_project(project_id)
    db.session.delete(project)
    db.session.commit()
    flash(f"Project {project.name} was deleted.")
    return redirect(url_for("project.index"))
