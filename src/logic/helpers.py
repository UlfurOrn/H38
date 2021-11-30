from __future__ import annotations

from pydantic import BaseModel


class ListItem(BaseModel):
    pass


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
            raise Exception(f"Page should be between 1 and {max_page}")

        return Paginator(
            page=page,
            total=total,
            max_page=max_page,
            items=items[(page - 1) * cls._PAGE_SIZE : page * cls._PAGE_SIZE],  # noqa
        )
