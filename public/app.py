from flask import Flask, render_template


app = Flask(__name__)


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
    app.run(host="0.0.0.0", port=8080, debug=True)
