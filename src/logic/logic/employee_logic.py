from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from database.models.employee_model import Employee
from logic.helpers import FilterOptions, InfoModel, ListItem, Paginator, filter_by_field
from utils.authentication import requires_supervisor


class EmployeeItem(ListItem):
    employee_id: UUID
    name: str
    ssn: int
    phone: int


class EmployeeInfo(InfoModel):
    employee_id: UUID
    name: str
    ssn: int
    address: str
    home_phone: Optional[int]
    work_phone: int
    email: str
    location_id: UUID
    location: str


class EmployeeCreate(BaseModel):
    name: str
    ssn: str
    address: str
    home_phone: Optional[str]
    work_phone: str
    email: str
    location_id: UUID

    @validator("home_phone", "work_phone")
    def validate_phone(cls, value):
        if value is not None:
            assert value.isdigit(), "Phone number should only include numbers"
            assert len(value) == 7, "Phone number should be exactly 7 digits"

        return value

    @validator("ssn")
    def validate_ssn(cls, value):
        assert value.isdigit(), "SSN should only include numbers"
        assert len(value) == 10, "SSN should be exactly 10 digits"

        employees = Employee.all()
        for employee in employees:
            assert employee.ssn != value, "User with this SSN already exists"

        return value


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    home_phone: Optional[str] = None
    work_phone: Optional[str] = None
    email: Optional[str] = None
    location_id: Optional[UUID] = None

    @validator("home_phone", "work_phone")
    def validate_phone(cls, value):
        if value is not None:
            assert value.isdigit(), "Phone number should only include numbers"
            assert len(value) == 7, "Phone number should be exactly 7 digits"

        return value


class EmployeeFilterOptions(FilterOptions):
    location_id: Optional[UUID]
    location: Optional[str]
    ssn: Optional[str]
    name: Optional[str]
    phone: Optional[str]


class EmployeeLogic:
    @staticmethod
    def all(page: int, filters: EmployeeFilterOptions, search: Optional[str] = None) -> Paginator:
        employees = Employee.all()

        if filters.location_id:
            employees = filter(lambda employee: filters.location_id == employee.location_id, employees)

        employees = filter_by_field(employees, "ssn", filters.ssn)
        employees = filter_by_field(employees, "name", filters.name)
        employees = filter_by_field(employees, "phone", filters.phone)

        employee_items = [
            EmployeeItem(employee_id=employee.id, name=employee.name, ssn=employee.ssn, phone=employee.work_phone)
            for employee in employees
        ]

        return Paginator.paginate(employee_items, page)

    @staticmethod
    def filter(page: int = 1, location_filter: UUID = None) -> Paginator:
        employees = Employee.all()

        filtered_list = [
            EmployeeItem(employee_id=employee.id, name=employee.name, ssn=employee.ssn, phone=employee.work_phone)
            for employee in employees
            if location_filter is not None and employee.location_id == location_filter
        ]

        return Paginator.paginate(filtered_list, page)

    @staticmethod
    @requires_supervisor
    def create(data: EmployeeCreate) -> UUID:
        employee = Employee(**data.dict())

        employee.create()

        return employee.id

    @staticmethod
    def get(employee_id: UUID) -> EmployeeInfo:
        employee = Employee.get(employee_id)
        location = employee.location

        return EmployeeInfo(
            employee_id=employee.id,
            name=employee.name,
            ssn=employee.ssn,
            address=employee.address,
            home_phone=employee.home_phone,
            work_phone=employee.work_phone,
            email=employee.email,
            location_id=location.id,
            location=location.country,
        )

    @staticmethod
    def update(employee_id: UUID, data: EmployeeUpdate) -> UUID:
        employee = Employee.get(employee_id)

        employee.name = data.name or employee.name
        employee.address = data.address or employee.address
        employee.home_phone = data.home_phone
        employee.work_phone = data.work_phone or employee.work_phone
        employee.email = data.email or employee.email
        employee.location_id = data.location_id or employee.location_id

        employee.update()

        return employee.id
