from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "Hello from Quickseal/api!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
