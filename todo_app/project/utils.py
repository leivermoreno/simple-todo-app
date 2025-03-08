from flask import abort, g
from sqlalchemy import select

from project.models import Project
from collaborator.models import Collaborator
from db import db
from utils import to_int


def get_project(project_id, check_collaborator=True):
    project_id = to_int(project_id)
    project = db.session.get(Project, project_id)

    if project is None:
        abort(404)

    elif project.user_id != g.user.id:
        if not check_collaborator or not is_collaborator(project_id):
            abort(403)

    return project


def is_collaborator(project_id):
    stmt = (
        select(Collaborator)
        .where(Collaborator.user_id == g.user.id)
        .where(Collaborator.project_id == project_id)
    )
    collaborator = db.session.scalar(stmt)
    if collaborator is not None:
        return True

    return False
