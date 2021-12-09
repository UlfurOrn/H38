from __future__ import annotations

from typing import Optional
from uuid import UUID

from database.models.database_model import DatabaseModel


class Location(DatabaseModel):
    _HEADERS = ["id", "country", "airport", "phone", "opening_hours", "supervisor_id"]
    _FILENAME = "locations.csv"

    country: str
    airport: str
    phone: int
    opening_hours: str
    supervisor_id: Optional[UUID] = None

    @classmethod
    def serialize(cls, model: Location) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Location:
        cls._optional(data, "supervisor_id")
        return Location(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"

    Location(
        country="Iceland",
        airport="Keflavík, Airport",
        phone=1234567,
        opening_hours="08:00-20:00",
        supervisor_id=UUID("c114a7b3-d5c9-490f-b82d-38709fe825f1"),
    ).create()

    print(Location.read())
