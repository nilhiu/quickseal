import os
from flask import Flask, render_template


app = Flask(__name__)
API_URL = os.environ.get("QUICKSEAL_API_URL")


@app.route("/")
def index():
    return render_template("index.j2")


@app.route("/broadcast")
def broadcast():
    return render_template("broadcast.j2", shares=[{"id": "some_id"}])


@app.route("/broadcast/<int:share_id>")
def files(share_id: int):
    return render_template("files.j2", share_id=share_id, files=["file.txt"])


if __name__ == "__main__":
    if API_URL is None:
        app.logger.fatal("environmental variable QUICKSEAL_API_URL was not provided")
        exit(1)
    app.run(host="0.0.0.0", port=8080, debug=True)
