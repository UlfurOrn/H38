from __future__ import annotations

from uuid import UUID

from database.models.database_model import DatabaseModel


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

    @classmethod
    def serialize(cls, model: Employee) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Employee:
        return Employee(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"

    Employee(
        name="Úlfur Örn Björnsson",
        ssn=2811002110,
        address="Heiðargerði 21",
        home_phone=5812345,
        work_phone=6627880,
        email="ulfurinn@gmail.com",
        location_id=UUID("c114a7b3-d5c9-490f-b82d-38709fe825f1"),
    ).create()

    print(Employee.read())
