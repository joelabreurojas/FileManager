from typing import Any, List

from ..models.entities import File
from ..models.exceptions import FileAlreadyExists, FileNotFound
from .connection import fetch_all, fetch_lastrow_id, fetch_none, fetch_one


def create(file: File) -> File:
    if __file_exists("description", file.description):  # type: ignore
        raise FileAlreadyExists(f"Description '{file.description}' is already used")

    query = """
        INSERT INTO documents
        VALUES (:description, :modification, :expiration, :extension, :label)
        """

    parameters = file._asdict()

    id = fetch_lastrow_id(query, parameters)

    parameters["id"] = id

    return File(**parameters)


def list_all() -> List[File]:
    query = "SELECT oid, * FROM documents ORDER BY description"
    records = fetch_all(query)
    if records is None:
        raise FileNotFound("No files in database")

    return __package_files(records)


def detail(file: File) -> List[File]:
    query = "SELECT oid, * FROM documents WHERE description LIKE ?"
    parameters = f"%{file.description}%"

    records = fetch_all(query, parameters)
    if records is None:
        raise FileNotFound(f"No file with description: {file.description}")

    return __package_files(records)


def update(file: File) -> File:
    query = """
        UPDATE documents
        SET description = :description, modification = :modification, expiration = :expiration, label = :label
        WHERE oid = :id
        """

    parameters = file._asdict()
    fetch_none(query, parameters)

    return file


def delete(file: File) -> File:
    query = "DELETE FROM documents WHERE oid = :id"
    parameters = file._asdict()
    fetch_none(query, parameters)

    return file


def reset_table() -> None:
    query = "DROP TABLE IF EXISTS documents"
    fetch_none(query)

    fields = "(description text, modification text, expiration text, extension text, label text)"
    query = f"CREATE TABLE IF NOT EXISTS documents {fields}"
    fetch_none(query)


def __file_exists(field: str, value: str) -> bool:
    query = f"SELECT oid, description from documents WHERE {field}=?"
    parameters = value

    record = fetch_one(query, parameters)

    return bool(record)


def __package_files(records: List[Any]) -> List[File]:
    files: List[File] = list()

    for record in records:
        file = File(
            id=record[0],
            description=record[1],
            modification=record[2],
            expiration=record[3],
            extension=record[4],
            label=record[5],
        )
        files.append(file)

    return files
