from flask import Flask
from flask_alembic import Alembic
from routes import routes
from db import db
from models import Model

app = Flask(__name__)
# TODO: Change the DB implementation to Postgres.
app.config["SQLALCHEMY_ENGINES"] = {"default": "sqlite:///api.db"}
db.init_app(app)
alembic = Alembic(app, metadatas=Model.metadata)


if __name__ == "__main__":
    app.register_blueprint(routes)
    app.run(host="0.0.0.0", port=8081, debug=True)
