import io
import os
from flask import Flask, render_template, send_file
import requests


app = Flask(__name__)
API_URL = os.environ.get("QUICKSEAL_API_URL")


@app.route("/")
def index():
    return render_template("index.j2")


@app.route("/broadcast")
def broadcast():
    resp = requests.get(f"{API_URL}/file_share")
    shares = resp.json()
    return render_template("broadcast.j2", share_ids=shares["file_shares"])


@app.route("/broadcast/<int:share_id>")
def files(share_id: int):
    resp = requests.post(f"{API_URL}/file_share/{share_id}")
    share = resp.json()
    return render_template("files.j2", share_id=share_id, files=share["files"])


@app.route("/broadcast/<int:share_id>/<string:filename>")
def file(share_id, filename):
    resp = requests.post(f"{API_URL}/file_share/{share_id}/{filename}")
    return send_file(
        io.BytesIO(resp.content),
        mimetype=resp.headers.get("Content-Type"),
        as_attachment=True,
        download_name=filename,
    )


if __name__ == "__main__":
    if API_URL is None:
        app.logger.fatal("environmental variable QUICKSEAL_API_URL was not provided")
        exit(1)
    app.run(host="0.0.0.0", port=8080, debug=True)
