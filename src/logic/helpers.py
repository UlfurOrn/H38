from __future__ import annotations

from pydantic import BaseModel


class ListItem:
    pass


class Paginator(BaseModel):
    _PAGE_SIZE = 10

    page: int
    total: int
    max_page: int
    items: list[ListItem]

    @classmethod
    def paginate(cls, items: list[ListItem], page: int) -> Paginator:
        return Paginator(
            page=page,
            total=len(items),
            max_page=(len(items) - 1) // cls._PAGE_SIZE if items else 0,
            items=items[(page - 1) * cls._PAGE_SIZE : page * cls._PAGE_SIZE],  # noqa
        )
