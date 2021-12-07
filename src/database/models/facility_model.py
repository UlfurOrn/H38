from __future__ import annotations

from uuid import UUID

from database.models.database_model import DatabaseModel


class Facility(DatabaseModel):
    _HEADERS = ["id", "property_id", "name", "condition"]
    _FILENAME = "facilities.csv"

    property_id: UUID
    name: str
    condition: str

    @classmethod
    def serialize(cls, model: Facility) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Facility:
        return Facility(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"
