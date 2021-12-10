from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from database.models.report_model import Report, ReportStatus
from database.models.request_model import RequestStatus
from logic.helpers import InfoModel, ListItem, Paginator
from utils.exceptions import BadRequestException


class ReportItem(ListItem):
    report_id: UUID
    property: str
    employee: str
    status: str


class ReportInfo(InfoModel):
    report_id: UUID
    request_id: UUID
    property_id: UUID
    property: str
    employee_id: UUID
    employee: str
    description: str
    cost: int
    contractors: int
    status: str


class ReportCreate(BaseModel):
    description: str
    cost: int


class ReportLogic:
    @staticmethod
    def all(page: int, search: Optional[str] = None) -> Paginator:
        reports = Report.all()

        def check_match(report):
            return search in str(report.id)

        if search is not None:
            reports = filter(check_match, reports)

        report_items = [
            ReportItem(
                report_id=report.id,
                property=report.request.property.property_number,
                employee=report.request.employee.name,
                status=report.status,
            )
            for report in reports
        ]

        return Paginator.paginate(report_items, page)

    @staticmethod
    def create(request_id: UUID, data: ReportCreate) -> UUID:
        report = Report(request_id=request_id, status=ReportStatus.Unapproved, **data.dict())

        report.create()

        return report.id

    @staticmethod
    def get(report_id: UUID) -> ReportInfo:
        report = Report.get(report_id)
        request = report.request
        property = request.property
        employee = request.employee

        return ReportInfo(
            report_id=report.id,
            request_id=request.id,
            property_id=property.id,
            property=property.property_number,
            employee_id=employee.id,
            employee=employee.name,
            description=report.description,
            cost=report.cost,
            contractors=len(request.contractor_requests),
            status=report.status,
        )

    @staticmethod
    def approve(report_id: UUID) -> None:
        report = Report.get(report_id)

        if report.status != ReportStatus.Unapproved:
            raise BadRequestException(f"Can't approve report with status: {report.status.value}")

        report.status = ReportStatus.Approved
        report.update()

    @staticmethod
    def unapprove(report_id: UUID) -> None:
        report = Report.get(report_id)

        if report.status != ReportStatus.Approved:
            raise BadRequestException(f"Can't unapprove report with status: {report.status.value}")

        report.status = ReportStatus.Unapproved
        report.update()

    @staticmethod
    def close(report_id: UUID) -> None:
        report = Report.get(report_id)

        if report.status != ReportStatus.Approved:
            raise BadRequestException(f"Can't close report with status: {report.status.value}")

        request = report.request

        report.status = ReportStatus.Closed
        request.status = RequestStatus.Closed

        report.update()
        request.update()

    @staticmethod
    def cancel(report_id: UUID) -> None:
        report = Report.get(report_id)

        if report.status != ReportStatus.Unapproved:
            raise BadRequestException(f"Can't cancel report with status: {report.status.value}")

        report.status = ReportStatus.Cancelled
        report.update()
