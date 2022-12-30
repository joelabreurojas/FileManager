"""Auxiliary tasks of the application"""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

import pendulum

from ..models.entities import File
from ..models.exceptions import FileAlreadyUsed, FileNotFound, FileNotValid

DATABASE = Path.cwd() / "filemanager" / "database" / "documents.db"
STORAGE = Path.cwd() / "filemanager" / "database" / ".storage"


def decompose_file(file: str) -> Tuple[str, str]:
    """From a file, filter out the description and extension"""

    description = Path(file).stem
    extension = Path(file).suffix
    return description, extension


def replace_text(text: str) -> str:
    """Remove invalid values and send the text in lower case"""

    text = re.sub(r"[^a-zA-Z0-9]", "", text)
    return text.lower()


def limit_text(text: str) -> str:
    """Limits the input according to a specified value"""

    limit = 25

    if len(text) > limit:
        text = text[0:limit] + "..."

    return text


def file_used(file_: File) -> None:
    """Displays an error message if the file is in use"""

    file_dict = file_._asdict()

    values = decompose_file(f"{file_.path}")
    file_dict["description"] = values[0]
    file_dict["extension"] = values[1]

    file = format_file(File(**file_dict))

    try:
        rename_file(file)

    except:
        raise FileAlreadyUsed(
            f"The file '{file.path}' is being used by another process."
        )


def validate_file(file: File) -> None:
    "Displays an error message if the data content of the file is invalid"

    if not __valid_text(file.description):
        raise FileNotValid(
            f"""
            The description "{file.description}" is not valid
            
            Indentifier rules :
            - Only lowercase letters (a-z), numbers (0-9) and underscore (_)
            - The first digit cannot be a number
            """
        )

    if not isinstance(file.extension, str) or not file.extension:
        raise FileNotValid(f"The extension '{file.extension}' is not valid")


def format_file(file: File) -> File:
    """Establishes the format to be used for the data in the files"""

    file_dict = file._asdict()

    file_dict["extension"] = file_dict["extension"].replace(".", "").upper()
    file_dict["modification"] = __format_date(r"YYYY/MM/DD LT")

    return File(**file_dict)


def copy_file(file: File) -> None:
    """Copy a file with a new name"""

    source = Path(f"{file.path}")
    destination = STORAGE / f"{file.description}.{file.extension}"

    shutil.copy(source, destination)
    os.system(f"attrib +h +s {destination}")


def open_file(file: File) -> None:
    """Finds a file in the local storage and opens it"""

    path = STORAGE / f"{file.description}.{file.extension}"
    subprocess.Popen([path], shell=True)


def rename_file(file: File) -> None:
    """Changes the name of a file"""

    path = STORAGE / f"{file.path}"
    path.rename(path.with_name(f"{file.description}.{file.extension}"))


def delete_file(file: File) -> None:
    """Deletes a file from the database and local storage"""

    path = STORAGE / f"{file.description}.{file.extension}"
    if path.exists():
        path.unlink()


def generate_backup(file: File) -> None:
    """Creates and classifies the backup of files in the local storage"""

    if not any(STORAGE.iterdir()):
        raise FileNotFound("No stored files found")

    date = __format_date("Y_M_D")
    source = STORAGE
    destiny = __folder_name(Path(f"{file.path}") / "Backups" / date)

    shutil.copytree(source, destiny)


def reset_database() -> None:
    """Delete the database and storage to create them again"""

    if DATABASE.exists():
        DATABASE.unlink()

    if STORAGE.exists():
        for file in STORAGE.iterdir():
            file.unlink()
        STORAGE.rmdir()

    DATABASE.touch()
    STORAGE.mkdir(parents=True, exist_ok=True)

    os.system(f"attrib +h +s {STORAGE}")


def __valid_text(text: Optional[str]) -> bool:
    """Checks if the text complies with the parameters"""

    if not isinstance(text, str) or not text:
        return False

    regex = r"^[a-z_][a-z_0-9]*$"

    return bool(re.search(regex, text))


def __format_date(format: str) -> str:
    """Returns the current date in the format received"""

    dt = pendulum.now()
    return dt.format(format)


def __folder_name(path: Path) -> Path:
    """Sets the name of the directory"""

    count = 1
    new_path = path / str(count)

    while new_path.exists():
        count += 1
        new_path = path / str(count)

    return new_path
