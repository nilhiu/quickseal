from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean, VARCHAR, ForeignKey


class Model(DeclarativeBase):
    pass


class File(Model):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_share_id: Mapped[int] = mapped_column(
        ForeignKey("file_shares.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(VARCHAR(), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"<File {self.name}>"


class FileShare(Model):
    __tablename__ = "file_shares"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    is_broadcast: Mapped[bool] = mapped_column(Boolean, nullable=False)
    password: Mapped[str] = mapped_column(VARCHAR(), nullable=True)
    files: Mapped[list[File]] = relationship()

    def __repr__(self):
        return f"<FileShare {self.id}>"
