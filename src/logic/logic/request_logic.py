from datetime import date, datetime, timedelta
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from database.models.request_model import Priority, Request, Status
from logic.helpers import InfoModel, ListItem, Paginator
from utils.exceptions import BadRequest


class RequestItem(ListItem):
    request_id: UUID
    property: str
    date: date
    priority: Priority
    status: Status


class RequestInfo(InfoModel):
    property_id: UUID
    location: str
    facility: str
    date: date
    priority: str


class SingleRequestCreate(BaseModel):
    property_id: UUID
    date: date
    priority: Priority


class MultipleRequestCreate(BaseModel):
    property_id: UUID
    start_date: date
    end_date: date
    interval: timedelta
    priority: Priority


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
            RequestItem(
                request_id=request.id,
                property=request.property.property_number,
                date=request.date,
                priority=request.priority,
                status=request.status,
            )
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
    def create(data: SingleRequestCreate) -> UUID:
        request = Request(**data.dict(), status=Status.Todo)

        request.create()

        return request.property_id

    @staticmethod
    def recurring(data: MultipleRequestCreate) -> UUID:
        start_date = data.start_date
        end_date = data.end_date

        if start_date < datetime.now():
            raise BadRequest("Start date must be in the future")

        if end_date < start_date:
            raise BadRequest("Start date must be before end date")

        first_request = None
        current_date = start_date
        while current_date <= end_date:
            request = Request(
                property_id=data.property_id, date=current_date, priority=data.priority, status=Status.Todo
            ).create()
            if first_request is None:
                first_request = request

        return first_request.id

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
