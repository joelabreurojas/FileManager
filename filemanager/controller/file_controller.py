"""Logical module for file management"""

from typing import List

from ..database import file_db
from ..helpers import util
from ..models.entities import File


def create(file_: File) -> None:
    """Validates the file before adding it to the database and local storage"""

    util.validate_file(file_)
    file = util.format_file(file_)
    file_db.create(file)
    util.copy_file(file)


def open(file: File) -> None:
    """Indicates the file to be opened"""

    util.open_file(file)


def update(file_: File) -> None:
    """Updates the file information after validation"""

    util.file_used(file_)
    util.validate_file(file_)
    file = util.format_file(file_)
    file_db.update(file)
    util.rename_file(file)


def lists() -> List[File]:
    """Sends the database records"""

    return file_db.list_all()


def details(file: File) -> List[File]:
    """Sends database records according to description"""

    return file_db.detail(file)


def delete(file: File) -> None:
    """Deletes the file if not in use"""

    util.file_used(file)
    file_db.delete(file)
    util.delete_file(file)


def backup(file: File) -> None:
    """Indicates the path to generate the backup"""

    util.generate_backup(file)


def reset() -> None:
    """Delete the database and the local storage to create them again"""

    util.reset_database()
    file_db.reset_table()
