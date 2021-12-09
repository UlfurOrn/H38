from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID

from database.models.database_model import DatabaseModel
from database.models.property_model import Property


class Priority(str, Enum):
    Now = "Now"
    Asap = "ASAP"
    Soon = "Soon"


class Status(str, Enum):
    Todo = "To Do"
    Ongoing = "Ongoing"
    Done = "Done"
    Closed = "Closed"


class Request(DatabaseModel):
    _HEADERS = ["id", "property_id", "date", "status", "priority", "employee_id"]
    _FILENAME = "requests.csv"

    property_id: UUID
    date: date
    priority: Priority
    status: Status
    employee_id: Optional[UUID]

    @property
    def property(self) -> Property:
        return Property.get(self.property_id)

    @classmethod
    def serialize(cls, model: Request) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Request:
        cls._deserialize(data, "employee_id")
        return Request(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"
