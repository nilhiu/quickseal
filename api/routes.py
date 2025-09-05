import base64
import os
from flask import Blueprint, jsonify, send_file, request, current_app
from sqlalchemy import text, select
from models import File, FileShare
from db import db


routes = Blueprint("routes", __name__)


@routes.route("/health", methods=["GET"])
def health_check():
    db_health = True
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        db_health = False

    return jsonify(
        {
            "api": "ok",
            "db_conn": "ok" if db_health else "not ok",
        }
    )


@routes.route("/upload", methods=["POST"])
def upload():
    req = request.get_json()
    files = req["files"]
    if len(files) == 0:
        current_app.logger.warning(f"no files provided in upload request: {req}")
        return jsonify({"error": "no files provided"}), 400

    file_share = FileShare(is_broadcast=True, password=None)
    db.session.add(file_share)
    db.session.flush()
    file_share_dir = current_app.config["UPLOAD_PATH"] + f"{file_share.id}/"
    os.makedirs(file_share_dir, 660, True)
    current_app.logger.info(f"file share created: {file_share.id}")

    filenames: list[str] = []
    try:
        for file in files:
            if file["name"] == "":
                continue
            file_path = file_share_dir + file["name"]
            filenames.append(file["name"])

            binary = base64.b64decode(file["binary"])
            file_size = len(binary)
            if file_size > 3 * pow(1024, 2):
                current_app.logger.error(
                    f"upload attempt file size: {file_size} > 3 MiB"
                )
                return jsonify({"error": f"file '{file['name']}' size too large"}), 400

            with open(file_path, "wb") as f:
                f.write(binary)

            f = File(file_share_id=file_share.id, name=file["name"], size=file_size)
            db.session.add(f)
            current_app.logger.info(f"file created for file share: {file_share.id}")
    except Exception as e:
        db.session.rollback()
        os.rmdir(file_share_dir)
        current_app.logger.error(f"upload exception occured: {e}")
        return jsonify({"error": "file upload failed"}), 500

    db.session.commit()
    current_app.logger.info(f"file share transaction committed: {file_share.id}")
    return (
        jsonify(
            {
                "file_share": file_share.id,
                "accepted_files": filenames,
            }
        ),
        201,
    )


@routes.route("/file_share", methods=["GET"])
def broadcast_file_shares():
    try:
        file_shares = db.session.scalars(
            select(FileShare).where(FileShare.is_broadcast)
        ).all()
    except Exception as e:
        current_app.logger.error(f"broadcast_file_share access exception occured: {e}")
        return (
            jsonify({"error": "server failed to fetch all broadcast file shares"}),
            500,
        )
    return jsonify({"file_shares": [file_share.id for file_share in file_shares]}), 200


# TODO: Add password protected file shares.
@routes.route("/file_share/<int:id>", methods=["POST"])
def file_share(id: int):
    try:
        file_share = db.session.scalar(select(FileShare).where(FileShare.id == id))
    except Exception as e:
        current_app.logger.error(f"file_share access exception occured: {e}")
        return jsonify({"error": "server failed to fetch file share"}), 500

    if file_share is None:
        return jsonify({"error": "file share not found"}), 404
    current_app.logger.info(f"file share accessed: {file_share.id}")

    return (
        jsonify(
            {
                "file_share": file_share.id,
                "files": [file.name for file in file_share.files],
                "sizes": [file.size for file in file_share.files],
            }
        ),
        200,
    )


# TODO: Add password protected file shares.
@routes.route("/file_share/<int:id>/<string:file>", methods=["POST"])
def file_share_file(id, file):
    file_path = f"{current_app.config['UPLOAD_PATH']}/{id}/{file}"
    if not os.path.exists(file_path):
        current_app.logger.error(
            f"file request on nonexistent file: {file}, on file share: {id}"
        )
        return jsonify({"error": "file doesn't exist in file share"}), 404
    return send_file(file_path, as_attachment=True), 200
