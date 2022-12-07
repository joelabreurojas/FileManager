import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

import pendulum

from ..models.entities import File
from ..models.exceptions import FileNotFound, FileNotValid

DATABASE = Path.cwd() / "filemanager" / "database" / "documents.db"
STORAGE = Path.cwd() / "filemanager" / "static" / ".storage"


def decompose_file(file: str) -> Tuple[str, str]:
    description = Path(file).stem
    extension = Path(file).suffix
    return description, extension


def format_file(file: File) -> File:
    if not isinstance(file.extension, str):
        return file

    file_dict = (file)._asdict()

    file_dict["extension"] = file.extension.replace(".", "").upper()
    file_dict["modification"] = __format_date(r"YYYY/MM/DD LT")

    if file.expiration == "//":
        file_dict["expiration"] = ""

    return File(**file_dict)


def validate_file(file: File) -> None:
    if not __valid_text(file.description):
        raise FileNotValid(
            f"""
            The description "{file.description}" is not valid
            
            Indentifier rules :
            - Only alphanumeric values (a-Z, 0-9) and underscore (_)
            - The first digit cannot be a number
            """
        )

    if not isinstance(file.extension, str):
        raise FileNotValid(f"The extension '{file.extension}' is not valid")

    if not __valid_date(file.expiration):
        raise FileNotValid(f"The expiration '{file.expiration}' is not valid")


def generate_dates() -> Tuple[List[str], List[str], List[str]]:
    init_year = pendulum.now().year

    year = [str(i) for i in range(init_year, init_year + 11)]
    month = [str(i) if i >= 10 else f"0{i}" for i in range(1, 13)]
    day = [str(i) if i >= 10 else f"0{i}" for i in range(1, 32)]

    return year, month, day


def expired_file(file: File) -> bool:
    if not isinstance(file.expiration, str) or not file.expiration:
        return False

    date = file.expiration.split("/")

    year = int(date[0])
    month = int(date[1])
    day = int(date[2])

    expiration_date = pendulum.datetime(year, month, day)
    actual_date = pendulum.now()
    return expiration_date <= actual_date


def copy_file(file: str, new_name: str) -> None:
    source = Path(file)
    destination = STORAGE

    shutil.copy(source, destination / new_name)


def open_file(file: str) -> None:
    destination = STORAGE / file
    subprocess.Popen([destination], shell=True)


def rename_file(file: str, new_name: str) -> None:
    path = STORAGE / file
    path.rename(path.with_name(new_name))


def delete_file(file: str) -> None:
    destination = STORAGE / file
    if destination.exists():
        destination.unlink()


def generate_backup(folder: Optional[str] = None) -> None:
    if not any(STORAGE.iterdir()):
        raise FileNotFound("No stored files found")

    date = __format_date("Y_M_D")

    path = __folder_path(folder)

    source = STORAGE
    destiny = __folder_name(path / "Backups" / date)

    shutil.copytree(source, destiny)


def create_database() -> None:
    DATABASE.touch()
    STORAGE.mkdir(parents=True, exist_ok=True)

    os.system(f"attrib +h {STORAGE}")


def __format_date(format: str) -> str:
    dt = pendulum.now()

    return dt.format(format)  # type: ignore


def __valid_text(text: Optional[str]) -> bool:
    if not isinstance(text, str):
        return False

    regex = r"^[a-zA-Z_][\w]*$"

    return bool(re.search(regex, text))


def __valid_date(date: Optional[str]) -> bool:
    if not isinstance(date, str) or not date:
        return True

    return bool(8 <= len(date) <= 10)


def __folder_path(folder: Optional[str] = None) -> Path:
    if folder:
        return Path(folder)

    return Path().home() / "Desktop"


def __folder_name(path: Path) -> Path:
    count = 1
    new_path = path / str(count)

    while new_path.exists():
        count += 1
        new_path = path / str(count)

    return new_path
