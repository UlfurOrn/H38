from __future__ import annotations

from typing import Optional
from uuid import UUID

from database.models.database_model import DatabaseModel


class Employee(DatabaseModel):
    _HEADERS = ["id", "name", "phone"]
    _FILENAME = "employees.csv"

    id: Optional[UUID] = None
    name: str
    phone: int

    @classmethod
    def serialize(cls, model: Employee) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Employee:
        return Employee(id=data["id"], name=data["name"], phone=data["phone"])


if __name__ == "__main__":
    employees = [
        Employee(name="Úlfur Örn Björnsson", phone=1234567),
        Employee(name="Silja Dögg Helgadóttir", phone=7654321),
    ]

    Employee.save(employees)
    print(Employee.read())
