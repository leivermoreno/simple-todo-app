import os
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, "todo.db")}',
    )

    app.config.from_pyfile("config.py", silent=True)
    app.config.from_prefixed_env()

    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize the database
    from db import db

    db.init_app(app)

    import models

    with app.app_context():
        db.create_all()

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    import auth

    app.register_blueprint(auth.bp)

    import project

    app.register_blueprint(project.bp)
    app.add_url_rule("/", endpoint="index")

    import task

    app.register_blueprint(task.bp)

    return app
