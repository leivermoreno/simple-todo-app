import functools
from flask import redirect, url_for, g


def login_required(view=None):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        if view is not None:
            return view(**kwargs)

    return wrapped
