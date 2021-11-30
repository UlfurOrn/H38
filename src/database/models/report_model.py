from __future__ import annotations
from datetime import date

from uuid import UUID

from database.models.database_model import DatabaseModel
from database.models.location_model import Location


class Report(DatabaseModel):
    _HEADERS = ["property", "employee", "description", "cost", "satus", "date"]
    _FILENAME = "reports.csv"

    property_id: UUID
    employee_id: UUID
    description: str
    cost: str
    status: str
    date: date

    @property
    def location(self) -> Location:
        return Location.get(model_id=self.location_id)

    @classmethod
    def serialize(cls, model: Report) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Report:
        return Report(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"