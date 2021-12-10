from __future__ import annotations

from typing import Iterator, Optional

from pydantic import BaseModel

from database.models.database_model import DatabaseModel
from utils.exceptions import BadRequestException


class ListItem(BaseModel):
    def get(self, key: str) -> str:
        return str(self.__getattribute__(key))


class InfoModel(BaseModel):
    def get(self, key: str) -> str:
        return str(self.__getattribute__(key))


class FilterOptions(BaseModel):
    def get(self, key: str) -> str:
        return str(self.__getattribute__(key))


class Paginator(BaseModel):
    _PAGE_SIZE = 10

    page: int
    total: int
    max_page: int
    items: list[ListItem]

    @classmethod
    def paginate(cls, items: list[ListItem], page: int) -> Paginator:
        total = len(items)
        max_page = ((total - 1) // cls._PAGE_SIZE) + 1 if items else 1

        if not (1 <= page <= max_page):
            raise BadRequestException(f"Page should be between 1 and {max_page}")

        return Paginator(
            page=page,
            total=total,
            max_page=max_page,
            items=items[(page - 1) * cls._PAGE_SIZE : page * cls._PAGE_SIZE],  # noqa
        )


def filter_by_field(models: Iterator, field: str, value: Optional[str] = None) -> Iterator:
    if value is None:
        return models
    value = value.lower()
    return filter(lambda model: value in str(model.__getattribute__(field)).lower(), models)
