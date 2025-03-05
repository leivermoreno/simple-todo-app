from flask import abort


def to_int(value):
    try:
        return int(value)
    except ValueError:
        abort(404)
