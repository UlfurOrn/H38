from __future__ import annotations
from datetime import date
from enum import Enum

from datetime import date
from uuid import UUID

from database.models.database_model import DatabaseModel
from database.models.location_model import Location
from src.utils.exceptions import *


class Report(DatabaseModel):
    _HEADERS = ["id", "property_id", "employee_id", "description", "cost", "status", "date", "contractor"]
    _FILENAME = "reports.csv"

    property_id: UUID
    employee_id: UUID
    description: str
    cost: str
    status: str
    date: date
    contractor_id: UUID

    @classmethod
    def serialize(cls, model: Report) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> Report:
        return Report(**data)

class Status(Enum):
    approve = "approve"
    unapprove = "unapprove"
    close = "close"
    
if __name__ == "__main__":
    DatabaseModel._PATH = "../data/"
