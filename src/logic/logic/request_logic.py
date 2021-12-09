import re
from datetime import date, datetime, timedelta
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from database.models.request_model import Priority, Request, Status
from logic.helpers import InfoModel, ListItem, Paginator
from utils.exceptions import BadRequest


class RequestItem(ListItem):
    request_id: UUID
    property: str
    date: str
    priority: str
    status: str


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

    @validator("start_date", "end_date", pre=True)
    def validate_date(cls, date_string: str) -> date:
        try:
            return datetime.strptime(date_string, "%d/%m/%y").date()
        except ValueError:
            raise ValueError("Invalid date provided, use format: DD/MM/YY")

    @validator("interval", pre=True)
    def validate_interval(cls, interval: str) -> timedelta:
        match = re.match(r"^(?P<years>\d)y (?P<months>\d)m (?P<days>\d)d$", interval)
        assert match is not None, "Interval must have the following format: 0y 2m 1d"

        years = int(match.group("years"))
        months = int(match.group("months"))
        days = int(match.group("days"))

        assert years >= 0, "You can't have a negative amount of years"
        assert months >= 0, "You can't have a negative amount of months"
        assert days >= 0, "You can't have a negative amount of days"

        return timedelta(days=years * 365 + months * 30 + days)


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
                date=datetime.strftime(request.date, "%d/%m/%y"),
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

        if start_date < datetime.now().date():
            raise BadRequest("Start date must be in the future")

        if end_date < start_date:
            raise BadRequest("Start date must be before end date")

        first_request = None
        current_date = start_date
        while current_date <= end_date:
            request = Request(
                property_id=data.property_id, date=current_date, priority=data.priority, status=Status.Todo
            ).create()

            current_date += data.interval

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
