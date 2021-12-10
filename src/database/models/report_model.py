from __future__ import annotations

from enum import Enum
from uuid import UUID

from database.models.database_model import DatabaseModel
from database.models.request_model import Request


class ReportStatus(str, Enum):
    Cancelled = "Cancelled"
    Approved = "Approved"
    Unapproved = "Unapproved"
    Closed = "Closed"


class Report(DatabaseModel):
    _HEADERS = ["id", "request_id", "description", "cost", "status"]
    _FILENAME = "reports.csv"

    request_id: UUID
    description: str
    cost: str
    status: ReportStatus

    @property
    def request(self) -> Request:
        return Request.get(self.request_id)

    @classmethod
    def serialize(cls, model: Report) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Report:
        return Report(**data)


if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"
