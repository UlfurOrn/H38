from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from database.models.database_model import DatabaseModel


@dataclass()
class Employee(DatabaseModel):
    HEADERS = ["id", "name", "phone"]
    FILENAME = "employees.csv"

    name: str
    phone: int
    id: Optional[str] = field(default=None)

    @classmethod
    def serialize(cls, model: Employee) -> dict:
        return {"id": model.id, "name": model.name, "phone": model.phone}

    @classmethod
    def deserialize(cls, data: dict) -> Employee:
        return Employee(id=data["id"], name=data["name"], phone=data["phone"])


if __name__ == "__main__":
    employees = [
        Employee(id="1", name="Úlfur Örn Björnsson", phone=1234567),
        Employee(id="2", name="Silja Dögg Helgadóttir", phone=7654321),
    ]

    Employee.save(employees)
    print(Employee.read())
