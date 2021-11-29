from __future__ import annotations

from uuid import UUID

from database.models.database_model import DatabaseModel
from database.models.location_model import Location


class Employee(DatabaseModel):
    _HEADERS = ["id", "name", "ssn", "address", "home_phone", "work_phone", "email", "location_id"]
    _FILENAME = "employees.csv"

    name: str
    ssn: int
    address: str
    home_phone: int
    work_phone: int
    email: str
    location_id: UUID

    @property
    def location(self) -> Location:
        return Location.get(model_id=self.location_id)

    @classmethod
    def serialize(cls, model: Employee) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Employee:
        return Employee(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"

    print(Employee.all())

    employee = Employee.all()[0]
    print(employee)
