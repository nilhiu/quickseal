from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.j2")


@app.route("/broadcast")
def broadcast():
    return render_template("broadcast.j2", shares=[{"id": "some_id"}])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
