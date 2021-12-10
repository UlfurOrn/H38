from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from database.models.property_model import Condition, Property
from logic.helpers import FilterOptions, InfoModel, ListItem, Paginator, filter_by_field


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


class PropertyFilterOptions(FilterOptions):
    location_id: Optional[UUID]
    location: Optional[str]
    condition: Optional[Condition]
    property_number: Optional[str]


class PropertyLogic:
    @staticmethod
    def all(page: int, filters: PropertyFilterOptions) -> Paginator:
        properties = Property.all()

        if filters.location_id:
            properties = filter(lambda property: property.location_id == filters.location_id, properties)
        if filters.condition:
            properties = filter(lambda property: property.condition == filters.condition, properties)

        properties = filter_by_field(properties, "property_number", filters.property_number)

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
    def filter(page: int = 1, location_filter: UUID = None) -> Paginator:
        properties = Property.all()

        filtered_list = [
            PropertyItem(property_id=property.property_id, location=property.location, condition=property.condition)
            for property in properties
            if location_filter is not None and property.location_id == location_filter
        ]

        return Paginator.paginate(filtered_list, page)

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
