from flask import Flask
from flask_migrate import Migrate
from routes import routes
from db import db

app = Flask(__name__)
# TODO: Change the DB implementation to Postgres.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api.db"
db.init_app(app)
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.register_blueprint(routes)
    app.run(host="0.0.0.0", port=8081, debug=True)
