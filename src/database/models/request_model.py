from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID

from database.models.contractor_model import Contractor
from database.models.contractor_requests_model import ContractorRequest
from database.models.database_model import DatabaseModel
from database.models.employee_model import Employee
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
    def employee(self) -> Employee:
        if self.employee_id:
            return Employee.get(self.employee_id)

    @property
    def contractor_requests(self) -> list[ContractorRequest]:
        return [
            contractor_request
            for contractor_request in ContractorRequest.all()
            if contractor_request.request_id == self.id
        ]

    @property
    def property(self) -> Property:
        return Property.get(self.property_id)

    @classmethod
    def serialize(cls, model: Request) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Request:
        cls._optional(data, "employee_id")
        return Request(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"
