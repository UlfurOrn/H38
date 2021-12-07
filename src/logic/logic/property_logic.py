from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from database.models.property_model import Condition, Property
from logic.helpers import InfoModel, ListItem, Paginator


class PropertyItem(ListItem):
    property_id: UUID
    property_number: str
    location: str
    condition: str


class PropertyInfo(InfoModel):
    property_id: UUID
    property_number: str
    area: int
    location_id: UUID
    location: str
    condition: str
    facilities: int


class PropertyCreate(BaseModel):
    property_number: str
    area: int
    location_id: UUID
    condition: str


class PropertyUpdate(BaseModel):
    area: Optional[int] = None
    condition: Optional[Condition] = None


class PropertyLogic:
    @staticmethod
    def all(page: int) -> Paginator:
        properties = Property.all()

        property_items = [
            PropertyItem(
                property_id=property.id,
                property_number=property.property_number,
                location=property.location.airport,
                condition=property.condition,
            )
            for property in properties
        ]

        return Paginator.paginate(property_items, page)

    @staticmethod
    def create(data: PropertyCreate) -> UUID:
        property = Property(**data.dict())

        property.create()

        return property.id

    @staticmethod
    def get(property_id: UUID) -> PropertyInfo:
        property = Property.get(property_id)

        return PropertyInfo(
            property_id=property.id,
            property_number=property.property_number,
            area=property.area,
            location_id=property.location.id,
            location=property.location.airport,
            condition=property.condition,
            facilities=len(property.facilities),
        )

    @staticmethod
    def update(property_id: UUID, data: PropertyUpdate) -> UUID:
        property = Property.get(property_id)

        property.area = data.area or property.area
        property.condition = data.condition or property.condition

        property.update()

        return property.id
