from typing import NamedTuple, Optional


class File(NamedTuple):
    id: Optional[int] = None
    description: Optional[str] = None
    modification: Optional[str] = None
    expiration: Optional[str] = None
    extension: Optional[str] = None
    label: Optional[str] = None
