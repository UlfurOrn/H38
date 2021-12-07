from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from database.models.facility_model import Facility
from database.models.property_model import Condition, Property
from logic.helpers import InfoModel, ListItem, Paginator


class FacilityItem(ListItem):
    facility_id: UUID
    name: str
    condition: str


class FacilityInfo(InfoModel):
    facility_id: UUID
    name: str
    condition: str
    property_id: UUID
    property: str


class FacilityCreate(BaseModel):
    name: str
    condition: Condition


class FacilityUpdate(BaseModel):
    name: Optional[str] = None
    condition: Optional[Condition] = None


class FacilityLogic:
    @staticmethod
    def all(property_id: UUID, page: int) -> Paginator:
        facilities = Facility.all()

        facilities = filter(lambda facility: facility.property_id == property_id, facilities)

        facility_items = [
            FacilityItem(facility_id=facility.id, name=facility.name, condition=facility.condition)
            for facility in facilities
        ]

        return Paginator.paginate(facility_items, page)

    @staticmethod
    def create(property_id: UUID, data: FacilityCreate) -> UUID:
        facility = Facility(property_id=property_id, **data.dict())

        facility.create()

        return facility.id

    @staticmethod
    def get(facility_id: UUID) -> FacilityInfo:
        facility = Facility.get(facility_id)
        property = Property.get(facility.property_id)

        return FacilityInfo(
            facility_id=facility.id,
            name=facility.name,
            condition=facility.condition,
            property_id=property.id,
            property=property.property_number,
        )

    @staticmethod
    def update(facility_id: UUID, data: FacilityUpdate) -> UUID:
        facility = Facility.get(facility_id)

        facility.name = data.name or facility.name
        facility.condition = data.condition or facility.condition

        facility.update()

        return facility.id
