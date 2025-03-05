from flask import abort, g

from project.models import Project
from db import db
from utils import to_int


def get_project(project_id):
    project_id = to_int(project_id)
    project = db.session.get(Project, project_id)
    if project is None or project.user_id != g.user.id:
        abort(404)

    return project
