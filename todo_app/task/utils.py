from flask import abort, g

from db import db
from utils import to_int
from task.models import Task
from project.utils import is_collaborator


def get_task(task_id, check_collaborator=True):
    task_id = to_int(task_id)
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404)
    if task.project.user_id != g.user.id:
        if not check_collaborator or not is_collaborator(task.project.id):
            abort(403)

    return task
