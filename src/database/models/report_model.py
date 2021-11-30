from __future__ import annotations
from datetime import date

from uuid import UUID

from database.models.database_model import DatabaseModel
from database.models.location_model import Location


class Report(DatabaseModel):
    _HEADERS = ["id", "property_id", "employee_id", "description", "cost", "status", "date"]
    _FILENAME = "reports.csv"

    property_id: UUID
    employee_id: UUID
    description: str
    cost: str
    status: str
    date: date

    @classmethod
    def serialize(cls, model: Report) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Report:
        return Report(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"