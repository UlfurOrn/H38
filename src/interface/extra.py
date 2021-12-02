from typing import Any, Callable, Optional

from pydantic import BaseModel


class Button(BaseModel):
    letter: str
    description: str
    function: Optional[Callable]
    hide: bool = False


class Return(BaseModel):
    levels: int
    data: Any


class Column(BaseModel):
    name: str
    field: str
    size: int


class Field(BaseModel):
    name: str
    field: str


class CreateField(Field):
    required: bool = True
    submenu: bool = False
