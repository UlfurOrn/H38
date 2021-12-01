from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from database.models.employee_model import Employee
from database.models.location_model import Location
from logic.helpers import ListItem, Paginator


class LocationItem(ListItem):
    location_id: UUID
    country: str
    airport: int


class LocationInfo(BaseModel):
    location_id: str
    country: str
    airport: str
    supervisor_id: UUID
    supervisor: str


class LocationCreate(BaseModel):
    country: str
    airport: str
    supervisor_id: UUID


class LocationUpdate(BaseModel):
    supervisor_id: Optional[UUID] = None


class LocationLogic:
    @staticmethod
    def all(page: int) -> Paginator:
        locations = Location.all()

        location_items = [
            LocationItem(location_id=location.id, country=location.country, airport=location.airport)
            for location in locations
        ]

        return Paginator.paginate(location_items, page)

    @staticmethod
    def create(data: LocationCreate) -> UUID:
        employee = Location(**data.dict())

        employee.create()

        return employee.id

    @staticmethod
    def get(location_id: UUID) -> LocationInfo:
        location = Location.get(location_id)
        supervisor = Employee.get(location.supervisor_id)

        return LocationInfo(
            location_id=location.id,
            country=location.country,
            airport=location.airport,
            supervisor_id=supervisor.id,
            supervisor=supervisor.name,
        )

    @staticmethod
    def update(location_id: UUID, data: LocationUpdate) -> UUID:
        location = Location.get(location_id)

        location.supervisor_id = data.supervisor_id or location.supervisor_id

        location.update()

        return location.id
