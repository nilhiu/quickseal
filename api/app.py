from flask import Flask
from flask_alembic import Alembic
from routes import routes
from db import db
from models import Model


alembic = Alembic(metadatas=Model.metadata)


def create_app() -> Flask:
    app = Flask(__name__)
    # TODO: Change the DB implementation to Postgres.
    app.config["SQLALCHEMY_ENGINES"] = {"default": "sqlite:///api.db"}
    # TODO: Make UPLOAD_PATH customizable via an env var.
    app.config["UPLOAD_PATH"] = "data/"
    db.init_app(app)
    alembic.init_app(app)
    app.register_blueprint(routes)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8081, debug=True)
