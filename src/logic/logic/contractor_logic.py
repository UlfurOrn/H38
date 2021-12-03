from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from database.models.contractor_model import Contractor
from logic.helpers import ListItem, Paginator


class ContractorItem(ListItem):
    contractor_id: UUID
    name: str
    location_id: UUID
    phone: int


class ContractorInfo(BaseModel):
    contractor_id: UUID
    name: str
    phone: int
    email: str
    opening_hours: str
    location_id: UUID
    location: str


class ContractorCreate(BaseModel):
    name: str
    phone: int
    email: str
    opening_hours: str
    location: str


class ContractorUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[int] = None
    email: Optional[str] = None
    opening_hours: Optional[str] = None
    location_id: Optional[int] = None


class ContracatorLogic:
    @staticmethod
    def all(page: int) -> Paginator:
        contractors = Contractor.all()

        contractor_items = [
            ContractorItem(contractor_id=contractor.id, name=contractor.name, phone=contractor.phone)
            for contractor in contractors
        ]

        return Paginator.paginate(contractor_items, page)

    @staticmethod
    def create(data: ContractorCreate) -> UUID:
        contractor = Contractor(**data.dict())

        contractor.create()

        return contractor.id

    @staticmethod
    def get(contractor_id: UUID) -> ContractorInfo:
        contractor = Contractor.get(contractor_id)
        location = contractor.location

        return ContractorInfo(
            contractor_id=contractor.id,
            name=contractor.name,
            phone=contractor.phone,
            email=contractor.email,
            opening_hours=contractor.opening_hours,
            location_id=location.id,
            location=location.countr,
        )

    @staticmethod
    def update(contractor_id: UUID, data: ContractorUpdate) -> UUID:
        contractor = Contractor.get(contractor_id)

        contractor.name = data.name or contractor.name
        contractor.phone = data.phone or contractor.phone
        contractor.email = data.email or contractor.email
        contractor.opening_hours = data.opening_hours or contractor.opening_hours
        contractor.location_id = data.location_id or contractor.location_id

        contractor.update()

        return contractor.id
