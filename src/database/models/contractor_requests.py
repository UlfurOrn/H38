from __future__ import annotations

from typing import Optional
from uuid import UUID

from database.models.database_model import DatabaseModel


class ContractorRequest(DatabaseModel):
    _HEADERS = ["id", "contractor_id", "request_id", "grade", "cost"]
    _FILENAME = "employees.csv"

    contractor_id: UUID
    request_id: UUID
    grade: Optional[int]
    cost: Optional[int]

    @classmethod
    def serialize(cls, model: ContractorRequest) -> dict:
        return model.dict()

    @classmethod
    def deserialize(cls, data: dict) -> ContractorRequest:
        cls._optional(data, "grade")
        cls._optional(data, "cost")
        return ContractorRequest(**data)
