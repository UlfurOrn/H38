from enum import Enum, auto
from typing import Callable, Optional

from pydantic import BaseModel

BACK = "back"


class Button(BaseModel):
    letter: str
    description: str
    function: Optional[Callable]
    hidden: bool = False
    supervisor: bool = False


class Column(BaseModel):
    name: str
    field: str
    size: int


class Field(BaseModel):
    name: str
    field: str
    required: bool = True
    mutable: bool = True
    submenu: bool = False


class WindowState(Enum):
    Normal: auto
    Select: auto
    Add: auto
    View: auto