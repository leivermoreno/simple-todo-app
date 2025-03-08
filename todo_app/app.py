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

    import auth.blueprint

    app.register_blueprint(auth.blueprint.bp)

    import project.blueprint

    app.register_blueprint(project.blueprint.bp)
    app.add_url_rule("/", endpoint="index")

    import task.blueprint

    app.register_blueprint(task.blueprint.bp)

    import collaborator.blueprint

    app.register_blueprint(collaborator.blueprint.bp)

    with app.app_context():
        db.create_all()

    return app
