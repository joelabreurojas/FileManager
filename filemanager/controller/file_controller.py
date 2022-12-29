from typing import List

from ..database import file_db
from ..helpers import util
from ..models.entities import File


def create(file_: File) -> None:
    file = util.format_file(file_)
    util.validate_file(file)
    file_db.create(file)


def update(file_: File) -> None:
    file = util.format_file(file_)
    util.validate_file(file)
    file_db.update(file)


def lists() -> List[File]:
    return file_db.list_all()


def details(file: File) -> List[File]:
    return file_db.detail(file)


def delete(file: File) -> None:
    file_db.delete(file)


def reset() -> None:
    util.reset_database()
    file_db.reset_table()
