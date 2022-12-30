"""Structures focused on the transmission of information throughout the application"""

from typing import NamedTuple, Optional


class File(NamedTuple):
    """Focused on information related to files, this class is immutable"""

    id: Optional[int] = None
    description: Optional[str] = None
    modification: Optional[str] = None
    expiration: Optional[str] = None
    extension: Optional[str] = None
    label: Optional[str] = None
    path: Optional[str] = None
