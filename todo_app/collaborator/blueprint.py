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

from auth.models import User
from collaborator.models import Collaborator
from project.utils import get_project
from db import db
from utils import to_int
from auth.utils import login_required


bp = Blueprint(
    "collaborator", __name__, url_prefix="/collaborator", template_folder="templates"
)

bp.before_request(login_required())


@bp.get("/")
def index():
    return render_template(
        "collaborator_index.html", collaborations=g.user.collaborations
    )


@bp.route("/add", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        project_id = request.form["project_id"]
        user_email = request.form["email"]
        error = None
        project = None

        if not project_id or not user_email:
            error = "Must provide a valid project id and email."

        if not error and user_email == g.user.email:
            error = "Cannot invite yourself."

        if not error:
            stmt = select(User).where(User.email == user_email)
            user = db.session.scalar(stmt)
            if user is None:
                error = f"Could not find a user for email {user_email}."

        if not error:
            project = get_project(project_id, check_collaborator=False)
            stmt = (
                select(Collaborator)
                .where(Collaborator.user_id == user.id)
                .where(Collaborator.project_id == project.id)
            )
            if db.session.scalar(stmt) is not None:
                error = "User already participating in project."

        if not error and project is not None:
            collaborator = Collaborator(user_id=user.id)
            project.collaborators.append(collaborator)
            db.session.commit()
            flash("User invited.")
            return redirect(url_for("project.show_details", project_id=project.id))

        flash(error)

    project = None
    if request.method == "GET":
        project_id = request.args["project_id"]
        project = get_project(project_id, check_collaborator=False)

    return render_template("create_collaborator.html", project=project)


@bp.get("/delete/<int:collaborator_id>")
def delete(collaborator_id):
    project_id = to_int(request.args["project_id"])
    # call to check project existence and ownership
    get_project(project_id, check_collaborator=False)

    stmt = select(Collaborator).where(Collaborator.id == collaborator_id)
    collaborator = db.session.scalar(stmt)
    if collaborator is None:
        abort(404)
    elif collaborator.project_id != project_id:
        abort(403)

    db.session.delete(collaborator)
    db.session.commit()

    return redirect(url_for("project.show_collaborators", project_id=project_id))
