from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from database.models.property_model import Property
from logic.helpers import ListItem, Paginator


class PropertyItem(ListItem):
    property_id: UUID
    location: str
    condition: str


class PropertyInfo(BaseModel):
    property_id: UUID
    property_number: str
    location: str
    condition: str
    facilities: str


class PropertyCreate(BaseModel):
    property_id: UUID
    propert_number: str
    location: str
    condition: str
    facilities: str


class PropertyUpdate(BaseModel):
    location: Optional[str] = None
    condition: Optional[str] = None
    facilities: Optional[str] = None


class PropertyLogic:
    @staticmethod
    def all(page: int) -> Paginator:
        properties = Property.all()

        property_items = [
            PropertyItem(property_id=property.property_id, location=property.location, condition=property.condition)
            for property in properties
        ]

        return Paginator.paginate(property_items, page)

    @staticmethod
    def create(data: PropertyCreate) -> UUID:
        property = Property(**data.dict())

        property.create()

        return property.property_id

    @staticmethod
    def get(property_id: UUID) -> PropertyInfo:
        property = Property.get(property_id)
        # location = property.location

        return PropertyInfo(
            property_id=property.property_id,
            property_number=property.property_number,
            location=property.location,
            condition=property.condition,
            facilities=property.facilities,
        )

    @staticmethod
    def update(property_id: UUID, data: PropertyUpdate) -> UUID:
        property = Property.get(property_id)

        property.location = data.location or property.location
        property.condition = data.condition or property.condition
        property.facilities = data.facilities or property.facilities

        property.update()

        return property.property_id
