from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import routes

app = Flask(__name__)
# TODO: Change the DB implementation to Postgres.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.register_blueprint(routes)
    app.run(host="0.0.0.0", port=8081, debug=True)
