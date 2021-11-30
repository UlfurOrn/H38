from typing import Optional
from uuid import UUID
from datetime import date
from pydantic import BaseModel

from database.models.facility_model import Facility
from logic.helpers import ListItem, Paginator


class FacilityItem(ListItem):
    facility_name: str
    condition: str


class FacilityInfo(BaseModel):
    property_id: UUID
    facility_name: str
    condition: str


class FacilityCreate(BaseModel):
    facility_name: str
    condition: str


class FacilityUpdate(BaseModel):
    facility_name: Optional[str] = None
    condition: Optional[str] = None


class FacilityLogic:
    @staticmethod
    def all(property_id: UUID, page: int) -> Paginator:
        facilities = Facility.all(property_id)

        facility_items = [
            FacilityItem(facility_name=facility.facility_name, condition=facility.condition)
            for facility in facilities
        ]

        return Paginator.paginate(facility_items, page)

    @staticmethod
    def create(data: FacilityCreate) -> UUID:
        facility = Facility(**data.dict())

        facility.create()

        return facility.property_id

    @staticmethod
    def get(property_id: UUID) -> FacilityInfo:
        facility = Facility.get(property_id)

        return FacilityInfo(
            property_id=facility.property_id,
            facility_name=facility.facility_name,
            condition=facility.condition
        )


    @staticmethod
    def update(property_id: UUID, data: FacilityUpdate) -> UUID:
        facility = Facility.get(property_id)

        facility.facility_name = data.facility_name or facility.facility_name
        facility.condition = data.condition or facility.condition
        
        facility.update()

        return facility.property_id