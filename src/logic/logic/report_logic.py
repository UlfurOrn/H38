from typing import Optional
from uuid import UUID
from datetime import date
from Verklegt_1.H38.src.database.models.location_model import Location

from pydantic import BaseModel

from database.models.report_model import Report
from database.models.property_model import Property
from database.models.employee_model import Employee
from Verklegt_1.H38.src.logic.helpers import ListItem, Paginator

class ReportItem(ListItem):
    report_id: UUID
    property_id: UUID
    status: str
    date: date

class ReportInfo(BaseModel):
    report_id: UUID
    property_id: UUID
    employee_id: UUID
    description: str
    cost: str
    status: str
    date: date

class ReportCreate(BaseModel):
    property_id: UUID
    employee_id: UUID
    description: str
    cost: str
    status: str
    date: date

class ReportUpdate(BaseModel):
    property_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    description: Optional[str] = None
    cost: Optional[str] = None
    date: Optional[date] = None

class ReportLogic:
    @staticmethod
    def all(page: int) -> Paginator:
        reports = Report.all()

        report_items = [
            ReportItem(report_id = report.id, property_id = report.propert_id, 
                       status = report.status, date = report.date)
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
            report_id = report.id,
            property_id = report.property_id,
            employee_id = report.employee_id,
            description = report.description,
            cost = report.cost,
            status = report.status,
            date = report.date
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

        report.update()

        return report.id

    @staticmethod
    def approve(report_id: UUID) -> UUID:
        pass

    @staticmethod
    def unapprove(report_id: UUID) -> UUID:
        pass

    @staticmethod
    def close(report_id: UUID) -> UUID:
        pass
