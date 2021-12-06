from __future__ import annotations

from typing import Optional
from uuid import UUID

from database.models.database_model import DatabaseModel
from database.models.location_model import Location


class Employee(DatabaseModel):
    _HEADERS = ["id", "name", "ssn", "address", "home_phone", "work_phone", "email", "location_id"]
    _FILENAME = "employees.csv"

    name: str
    ssn: int
    address: str
    home_phone: Optional[int]
    work_phone: int
    email: str
    location_id: UUID

    @property
    def location(self) -> Location:
        return Location.get(model_id=self.location_id)

    def is_supervisor(self) -> bool:
        locations = Location.all()
        for location in locations:
            if location.supervisor_id == self.id:
                return True

        return False

    @classmethod
    def serialize(cls, model: Employee) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Employee:
        home_phone = data["home_phone"]
        if home_phone == "":
            data["home_phone"] = None
        return Employee(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"

    print(Employee.all())

    employee = Employee.all()[0]
    print(employee)
