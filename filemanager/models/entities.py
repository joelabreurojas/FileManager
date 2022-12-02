from typing import NamedTuple


class File(NamedTuple):
    id: int = 0
    description: str = ""
    modification: str = ""
    expiration: str = ""
    extension: str = ""
    label: str = ""
