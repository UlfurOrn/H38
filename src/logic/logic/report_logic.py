import enum
from typing import Optional
from uuid import UUID
from datetime import date
from enum import Enum

from pydantic import BaseModel

from database.models.report_model import *
from database.models.property_model import Property
from database.models.employee_model import Employee
from database.models.contractor_model import *
from src.utils.exceptions import NotFoundException
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
    contractor_id: UUID

class ReportCreate(BaseModel):
    property_id: UUID
    employee_id: UUID
    description: str
    cost: str
    status: str
    date: date
    contractor_id: UUID

class ReportUpdate(BaseModel):
    property_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    description: Optional[str] = None
    cost: Optional[str] = None
    date: Optional[date] = None
    contractor_id: Optional[UUID] = None

class ReportLogic:
    @staticmethod
<<<<<<< HEAD
    def all(page: int, search=None) -> Paginator:
        reports = Report.all()

        def check_match(search):
            if reports.id == search:
                return True
            
            return False

        if search is not None:
            reports = filter(check_match, reports)

=======
    def all(page: int) -> Paginator:
        reports = Report.all()

>>>>>>> main
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
            date = report.date,
            contractor_id = report.contractor_id
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
