from flask import Blueprint, flash, redirect, render_template, request, url_for

from db import db
from task.models import Task
from project.utils import get_project
from task.utils import get_task
from auth.utils import login_required


bp = Blueprint("task", __name__, url_prefix="/task", template_folder="templates")

bp.before_request(login_required())


@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        project_id = request.form["project_id"]
        text = request.form["text"]
        completed = "completed" in request.form
        error = None

        if not project_id or not text:
            error = "Must send valid values for project ID, text, and completed."

        if not error:
            project = get_project(project_id)
            task_id = request.form.get("task_id")
            if task_id is not None:
                task = get_task(task_id)
                task.text = text
                task.completed = completed
            else:
                task = Task(text=text, completed=False)
                project.tasks.append(task)

            db.session.commit()
            flash(f"Task was {"updated" if task_id else "created"}.")
            return redirect(url_for("project.show_details", project_id=project_id))

        flash(error)

    project_id = None
    task = None
    if request.method == "GET":
        project_id = request.args["project_id"]
        # to check that project exists and ownership or collaborator
        get_project(project_id)
        task_id = request.args.get("task_id")
        if task_id is not None:
            task = get_task(task_id)

    return render_template("create_task.html", project_id=project_id, task=task)


@bp.get("/completed/<int:task_id>")
def completed(task_id):
    task = get_task(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("project.show_details", project_id=task.project_id))


@bp.get("/delete/<int:task_id>")
def delete(task_id):
    project_id = request.args["project_id"]
    task = get_task(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task was deleted.")
    return redirect(url_for("project.show_details", project_id=project_id))
