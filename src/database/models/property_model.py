from __future__ import annotations

from uuid import UUID

from database.models.database_model import DatabaseModel
from database.models.location_model import Location


class Property(DatabaseModel):
    _HEADERS = ["id", "condition", "location_id"]
    _FILENAME = "properties.csv"

    property_number: str
    condition: str
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
    DatabaseModel._PATH = "../data/"

    property = Property(
        property_number = "property1234",
        condition = "good",
        location_id = "cd314c5c-1cc3-4376-9003-6529b14cda8f")
