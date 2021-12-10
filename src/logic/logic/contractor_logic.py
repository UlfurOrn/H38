from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.errors import DateTimeError

from database.models.contractor_model import Contractor
from logic.helpers import InfoModel, ListItem, Paginator


class ContractorItem(ListItem):
    contractor_id: UUID
    name: str
    location: str
    phone: int


class ContractorInfo(InfoModel):
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
    location_id: UUID

    @validator("phone")
    def validate_phone(cls, value):
        if not value:
            pass
        else:
            if not len(value) == 7 or not value.isadigit():
                raise ValueError("Phone number is incvalid! It should be the length of 7 numbers!")
        return value

    @validator("opening_hours")
    def validate_open_hours(cls, value):
        try:
            time_list = value.split("-")
            for time in time_list:
                time = time.strip(" ")
                datetime.strptime(time, "%H:%M")
        except ValueError:
            raise ValueError("Opening hours should be the format of: HH:MM - HH:MM")
        return value


class ContractorUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[int] = None
    email: Optional[str] = None
    opening_hours: Optional[str] = None
    location_id: Optional[UUID] = None

    @validator("phone")
    def validate_phone(cls, value):
        if not value:
            pass
        else:
            if not len(value) == 7 or not value.isadigit():
                raise ValueError("Phone number is incvalid! It should be the length of 7 numbers!")
        return value

    @validator("opening_hours")
    def validate_open_hours(cls, value):
        try:
            time_list = value.split("-")
            for time in time_list:
                time = time.strip(" ")
                datetime.strptime(time, "%H:%M")
        except ValueError:
            raise ValueError("Opening hours should be the format of: HH:MM - HH:MM")
        return value


class ContractorLogic:
    @staticmethod
    def all(page: int, search: Optional[str] = None) -> Paginator:
        contractors = Contractor.all()

        def check_match(contractor: Contractor):
            return search in str(contractor.name)

        if search:
            contractors = filter(check_match, contractors)

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
            location=location.airport,
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
