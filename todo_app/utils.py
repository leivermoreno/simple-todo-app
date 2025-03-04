from flask import abort, g

from db import db
from models import Project, Task


def to_int(value):
    try:
        return int(value)
    except ValueError:
        abort(404)


def get_project(project_id):
    project_id = to_int(project_id)
    project = db.session.get(Project, project_id)
    if project is None or project.user_id != g.user.id:
        abort(404)

    return project


def get_task(task_id):
    task_id = to_int(task_id)
    task = db.session.get(Task, task_id)
    if task is None or task.project.user_id != g.user.id:
        abort(404)

    return task
