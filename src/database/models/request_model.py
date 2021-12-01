from __future__ import annotations
from datetime import date

from uuid import UUID

from database.models.database_model import DatabaseModel
from database.models.location_model import Location


class Request(DatabaseModel):
    _HEADERS = ["id", "property_id", "status", "priority", "date"]
    _FILENAME = "requests.csv"

    property_id: UUID
    status: str
    priority: str
    date: date
    

    @classmethod
    def serialize(cls, model: Request) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Request:
        return Request(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"