import re
from datetime import date, datetime, timedelta
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from database.models.contractor_model import Contractor
from database.models.contractor_requests_model import ContractorRequest
from database.models.request_model import Priority, Request, Status
from logic.helpers import InfoModel, ListItem, Paginator
from logic.logic.contractor_logic import ContractorItem
from utils.authentication import AuthManager
from utils.exceptions import BadRequest


class RequestItem(ListItem):
    request_id: UUID
    property: str
    date: str
    priority: str
    status: str


class RequestInfo(InfoModel):
    request_id: UUID
    property_id: UUID
    property: str
    date: date
    priority: str
    status: str
    employee_id: Optional[UUID]
    employee: Optional[str]
    contractors: int


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
            date_object = datetime.strptime(date_string, "%d/%m/%y").date()
            if date_object < datetime.now().date():
                raise ValueError("Date cannot be in the past")
            return date_object
        except ValueError:
            raise ValueError("Invalid date provided, use format: DD/MM/YY")

    @validator("interval", pre=True)
    def validate_interval(cls, interval: str) -> timedelta:
        match = re.match(r"^(?P<years>\d+)y (?P<months>\d+)m (?P<weeks>\d+)w (?P<days>\d+)d$", interval)
        assert match is not None, "Interval must have the following format: 0y 2m 0w 1d"

        years = int(match.group("years"))
        months = int(match.group("months"))
        weeks = int(match.group("weeks"))
        days = int(match.group("days"))

        assert years >= 0, "You can't have a negative amount of years"
        assert months >= 0, "You can't have a negative amount of months"
        assert weeks >= 0, "You can't have a negative amount of weeks"
        assert days >= 0, "You can't have a negative amount of days"

        return timedelta(days=years * 365 + months * 30 + weeks * 7 + days)


class RequestUpdate(BaseModel):
    date: Optional[date] = None
    priority: Optional[Priority] = None

    @validator("date", pre=True)
    def validate_optional_date(cls, date_string: Optional[str] = None):
        if date_string is None:
            return
        try:
            date_object = datetime.strptime(date_string, "%d/%m/%y").date()
            if date_object < datetime.now().date():
                raise ValueError("Date cannot be in the past")
            return date_object
        except ValueError:
            raise ValueError("Invalid date provided, use format: DD/MM/YY")


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
    def get(request_id: UUID) -> RequestInfo:
        request = Request.get(request_id)
        property = request.property

        employee = request.employee
        if employee is not None:
            employee = employee.name

        return RequestInfo(
            request_id=request.id,
            property_id=property.id,
            property=property.property_number,
            date=request.date,
            priority=request.priority,
            status=request.status,
            employee_id=request.employee_id,
            employee=employee,
            contractors=len(request.contractor_requests),
        )

    @staticmethod
    def update(request_id: UUID, data: RequestUpdate) -> UUID:
        request = Request.get(request_id)

        request.date = data.date or request.date
        request.priority = data.priority or request.priority

        request.update()

        return request.property_id

    @staticmethod
    def contractors(request_id: UUID, page: int = 1) -> Paginator:
        request = Request.get(request_id)
        contractors = [
            Contractor.get(contractor_request.contractor_id) for contractor_request in request.contractor_requests
        ]

        contractor_items = [
            ContractorItem(
                contractor_id=contractor.id,
                name=contractor.name,
                location=contractor.location.country,
                phone=contractor.phone,
            )
            for contractor in contractors
        ]

        return Paginator.paginate(contractor_items, page)

    @staticmethod
    def add_contractor(request_id: UUID, contractor_id: UUID) -> None:
        request = Request.get(request_id)
        contractor = Contractor.get(contractor_id)

        contractor_ids = [contractor_request.contractor_id for contractor_request in request.contractor_requests]

        if contractor.id in contractor_ids:
            raise BadRequest("Contractor is already assigned to this task")

        ContractorRequest(request_id=request.id, contractor_id=contractor.id).create()

    @staticmethod
    def assign(request_id: UUID) -> None:
        request = Request.get(request_id)

        if request.status != Status.Todo:
            raise BadRequest("Task has already been assigned")

        request.status = Status.Ongoing
        request.employee_id = AuthManager.get_user().id

        request.update()

    @staticmethod
    def done(request_id: UUID) -> None:
        request = Request.get(request_id)

        if request.status != Status.Ongoing:
            raise BadRequest("Task must have status ongoing")

        request.status = Status.Done

        request.update()
