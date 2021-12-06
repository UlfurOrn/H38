from __future__ import annotations

from enum import Enum
from uuid import UUID

from database.models.database_model import DatabaseModel
from database.models.location_model import Location


class Condition(str, Enum):
    Excellent = "Excellent"
    Good = "Good"
    OK = "OK"
    Bad = "Bad"
    Terrible = "Terrible"


class Property(DatabaseModel):
    _HEADERS = ["id", "property_number", "area", "condition", "location_id"]
    _FILENAME = "properties.csv"

    property_number: str
    area: int
    condition: Condition
    location_id: UUID

    @property
    def location(self) -> Location:
        return Location.get(model_id=self.location_id)

    def facilities(self):
        pass

    @classmethod
    def serialize(cls, model: Property) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Property:
        return Property(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "./data/"

    Property(
        property_number="property1234",
        area=100,
        condition=Condition.Good,
        location_id=UUID("cd314c5c-1cc3-4376-9003-6529b14cda8f"),
    ).create()
