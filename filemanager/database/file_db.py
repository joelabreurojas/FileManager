"""Database management for the documents table"""

from typing import Any, List

from ..models.entities import File
from ..models.exceptions import FileAlreadyExists
from .connection import fetch_all, fetch_none, fetch_one


def create(file: File) -> None:
    """Create a new file"""

    if __file_exists("description", file.description):  # type: ignore
        raise FileAlreadyExists(f"Description '{file.description}' is already used")

    query = """
        INSERT INTO documents
        VALUES (:description, :modification, :extension, :label)
        """

    parameters = file._asdict()
    fetch_none(query, parameters)


def list_all() -> List[File]:
    """Return all files in the table"""

    query = "SELECT oid, * FROM documents ORDER BY description"
    records = fetch_all(query)

    return __package_files(records)


def detail(file: File) -> List[File]:
    """Returns all files that match with the description"""

    query = "SELECT oid, * FROM documents WHERE description LIKE ?"
    parameters = f"%{file.description}%"

    records = fetch_all(query, parameters)

    return __package_files(records)


def update(file: File) -> None:
    """Update data of a selected file"""

    query = """
        UPDATE documents
        SET description = :description, modification = :modification, label = :label
        WHERE oid = :id
        """

    parameters = file._asdict()
    fetch_none(query, parameters)


def delete(file: File) -> None:
    """Delete a selected file"""

    query = "DELETE FROM documents WHERE oid = :id"
    parameters = file._asdict()
    fetch_none(query, parameters)


def reset_table() -> None:
    """Re-create the document table, if it already exists, delete it"""

    query = "DROP TABLE IF EXISTS documents"
    fetch_none(query)

    fields = "(description text, modification text, extension text, label text)"
    query = f"CREATE TABLE IF NOT EXISTS documents {fields}"
    fetch_none(query)


def __file_exists(field: str, value: str) -> bool:
    """Check if a parameter exists"""

    query = f"SELECT oid, description from documents WHERE {field}=?"
    parameters = value

    record = fetch_one(query, parameters)

    return bool(record)


def __package_files(records: List[Any]) -> List[File]:
    """Receives a list of data and returns it in a list of objects"""

    files: List[File] = list()

    for record in records:
        file = File(
            id=record[0],
            description=record[1],
            modification=record[2],
            extension=record[3],
            label=record[4],
        )
        files.append(file)

    return files
