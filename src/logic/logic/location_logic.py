from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from database.models.employee_model import Employee
from database.models.location_model import Location
from logic.helpers import FilterOptions, InfoModel, ListItem, Paginator, filter_by_field


class LocationItem(ListItem):
    location_id: UUID
    country: str
    airport: str


class LocationInfo(InfoModel):
    location_id: UUID
    country: str
    airport: str
    phone: int
    opening_hours: str
    supervisor_id: Optional[UUID]
    supervisor: Optional[str]


class LocationCreate(BaseModel):
    country: str
    airport: str
    phone: int
    opening_hours: str
    supervisor_id: Optional[UUID]


class LocationUpdate(BaseModel):
    airport: str
    phone: int
    opening_hours: str
    supervisor_id: Optional[UUID] = None


class LocationFilterOptions(FilterOptions):
    country: Optional[str]
    airport: Optional[str]
    phone: Optional[str]


class LocationLogic:
    @staticmethod
    def all(page: int, filters: LocationFilterOptions) -> Paginator:
        locations = Location.all()

        locations = filter_by_field(locations, "country", filters.country)
        locations = filter_by_field(locations, "airport", filters.airport)
        locations = filter_by_field(locations, "phone", filters.phone)

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
        supervisor_id = location.supervisor_id

        supervisor = None
        if supervisor_id is not None:
            supervisor = Employee.get(supervisor_id).name

        return LocationInfo(
            location_id=location.id,
            country=location.country,
            airport=location.airport,
            phone=location.phone,
            opening_hours=location.opening_hours,
            supervisor_id=supervisor_id,
            supervisor=supervisor,
        )

    @staticmethod
    def update(location_id: UUID, data: LocationUpdate) -> UUID:
        location = Location.get(location_id)

        location.airport = data.airport or location.airport
        location.phone = data.phone or location.phone
        location.opening_hours = data.opening_hours or location.opening_hours
        location.supervisor_id = data.supervisor_id

        location.update()

        return location.id
