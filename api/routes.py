from flask import Blueprint, jsonify

routes = Blueprint("routes", __name__)


@routes.route("/health")
def healthCheck():
    return jsonify({"health": "ok"})


@routes.route("/")
def index():
    return jsonify({"message": "Hello from Quickseal/api!"})
