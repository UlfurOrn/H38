from enum import Enum, auto
from typing import Callable

from pydantic import BaseModel

BACK = "back"


class WindowState(Enum):
    Normal = auto
    Select = auto
    View = auto
    Add = auto


class Button(BaseModel):
    letter: str
    description: str
    function: Callable
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
