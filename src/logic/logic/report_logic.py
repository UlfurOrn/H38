from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic.class_validators import validator
from utils.exceptions import BadRequest
from database.models.report_model import Status

from database.models.report_model import Report
from logic.helpers import InfoModel, ListItem, Paginator

from datetime import datetime


class ReportItem(ListItem):
    report_id: UUID
    property_id: UUID
    status: str
    date: date


class ReportInfo(InfoModel):
    report_id: UUID
    property_id: UUID
    employee_id: UUID
    description: str
    cost: str
    status: str
    date: date
    contractor_id: UUID


class ReportCreate(BaseModel):
    property_id: UUID
    employee_id: UUID
    description: str
    cost: str
    status: str
    date: date
    contractor_id: UUID

    @validator('date', pre=True)
    def validate_date(cls, value):
        try:
            date_list = value.split("-")
            for date in date_list:
                date = date.strip(" ")
                return datetime.strptime(date, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError('Date should be the format of: DD/MM/YYYY')


class ReportUpdate(BaseModel):
    property_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    description: Optional[str] = None
    cost: Optional[str] = None
    date: Optional[date] = None
    contractor_id: Optional[UUID] = None

    @validator('date', pre=True)
    def validate_date(cls, value):
        try:
            date_list = value.split("-")
            for date in date_list:
                date = date.strip(" ")
                return datetime.strptime(date, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError('Date should be the format of: DD/MM/YYYY')


class ReportLogic:
    @staticmethod
    def all(page: int, search: Optional[str] = None) -> Paginator:
        reports = Report.all()

        def check_match(report):
            return search in str(report.id)

        if search is not None:
            reports = filter(check_match, reports)

        report_items = [
            ReportItem(report_id=report.id, property_id=report.propert_id, status=report.status, date=report.date)
            for report in reports
        ]

        return Paginator.paginate(report_items, page)

    @staticmethod
    def create(data: ReportCreate) -> UUID:
        report = Report(**data.dict())

        report.create()

        return report.id

    @staticmethod
    def get(report_id: UUID) -> ReportInfo:
        report = Report.get(report_id)

        return ReportInfo(
            report_id=report.id,
            property_id=report.property_id,
            employee_id=report.employee_id,
            description=report.description,
            cost=report.cost,
            status=report.status,
            date=report.date,
            contractor_id=report.contractor_id,
        )

    @staticmethod
    def update(report_id: UUID, data: ReportUpdate) -> UUID:
        report = Report.get(report_id)

        report.property_id = data.property_id or report.property_id
        report.employee_id = data.employee_id or report.employee_id
        report.descriptrion = data.description or report.description
        report.cost = data.cost or report.cost
        report.status = data.status or report.status
        report.date = data.date or report.date
        report.contracor_id = data.contractor_id or report.contractor_id

        report.update()

        return report.id

    @staticmethod
    def approve(report_id: UUID) -> UUID:
        report = Report.get(report_id)

        if report.status == Status.unapprove:
            report.status = Status.approve
        else:
            raise BadRequest()

    @staticmethod
    def unapprove(report_id: UUID) -> UUID:
        report = Report.get(report_id)

        if report.status == Status.approve:
            report.status = Status.unapprove
        else:
            raise BadRequest()

    @staticmethod
    def close(report_id: UUID) -> UUID:
        report = Report.get(report_id)

        if report.status == Status.approve:
            report.status = Status.close
        else:
            raise BadRequest()
