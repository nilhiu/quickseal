from db import db


class FileShare(db.Model):
    __tablename__ = "file_shares"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_broadcast = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.VARCHAR(), nullable=True)
    files = db.relationship("File", lazy=True)

    def __repr__(self):
        return f"<FileShare {self.id}>"


class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_share_id = db.Column(
        db.Integer, db.ForeignKey("file_shares.id"), nullable=False
    )
    name = db.Column(db.VARCHAR(), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<File {self.name}>"
