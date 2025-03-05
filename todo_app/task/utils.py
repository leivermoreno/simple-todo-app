from flask import abort, g

from db import db
from utils import to_int
from task.models import Task


def get_task(task_id):
    task_id = to_int(task_id)
    task = db.session.get(Task, task_id)
    if task is None or task.project.user_id != g.user.id:
        abort(404)

    return task
