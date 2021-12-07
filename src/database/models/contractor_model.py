from __future__ import annotations

from uuid import UUID

from database.models.database_model import DatabaseModel
from database.models.location_model import Location


class Contractor(DatabaseModel):
    _HEADERS = ["id", "name", "phone", "opening_hours", "email", "location_id"]
    _FILENAME = "contractors.csv"

    name: str
    phone: int
    opening_hours: str
    email: str
    location_id: UUID

    @property
    def location(self) -> Location:
        return Location.get(model_id=self.location_id)

    @classmethod
    def serialize(cls, model: Contractor) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Contractor:
        return Contractor(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "./data/"

    Contractor(
        name="Test Contractor",
        phone=1234567,
        opening_hours="08:00-20:00",
        email="test@test.com",
        location_id=UUID("cd314c5c-1cc3-4376-9003-6529b14cda8f"),
    ).create()
