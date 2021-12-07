from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from database.models.request_model import Request
from logic.helpers import InfoModel, ListItem, Paginator


class RequestItem(ListItem):
    property_id: UUID
    facility: str
    priority: str


class RequestInfo(InfoModel):
    property_id: UUID
    location: str
    facility: str
    date: date
    priority: str


class RequestCreate(BaseModel):
    recurring: str
    date: date
    repetition: str
    final_date: str
    property_id: UUID
    location: str
    facility: str
    priority: str


class RequestUpdate(BaseModel):
    location: Optional[str] = None
    facility: Optional[str] = None
    date: Optional[date] = None
    priority: Optional[str] = None


class RequestLogic:
    @staticmethod
    def all(page: int) -> Paginator:
        requests = Request.all()

        request_items = [
            RequestItem(property_id=request.property_id, facility=request.facility, priority=request.priority)
            for request in requests
        ]

        return Paginator.paginate(request_items, page)

    @staticmethod
    def filter(page: int = 1, property_filter: UUID = None, employee_filter: UUID = None):
        requests = Request.all()

        filtered_list = [
            RequestItem(property_id=request.property_id, facility=request.facility, priority=request.priority)
            for request in requests
            if property_filter is not None
            and request.property_id == property_filter
            or employee_filter is not None
            and request.employee_id == employee_filter
        ]

        return Paginator.paginate(filtered_list, page)

    @staticmethod
    def create(data: RequestCreate) -> UUID:
        request = Request(**data.dict())

        request.create()

        return request.property_id

    @staticmethod
    def get(property_id: UUID) -> RequestInfo:
        request = Request.get(property_id)

        return RequestInfo(
            property_id=request.property_id,
            location=request.location,
            facility=request.facility,
            date=request.date,
            priority=request.priority,
        )

    @staticmethod
    def update(property_id: UUID, data: RequestUpdate) -> UUID:
        request = Request.get(property_id)

        request.location = data.location or request.location
        request.facility = data.facility or request.facility
        request.date = data.date or request.date

        request.update()

        return request.property_id
