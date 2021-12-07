from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from database.models.employee_model import Employee
from logic.helpers import InfoModel, ListItem, Paginator


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
    ssn: int
    address: str
    home_phone: Optional[int]
    work_phone: int
    email: str
    location_id: UUID


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    home_phone: Optional[int] = None
    work_phone: Optional[int] = None
    email: Optional[str] = None
    location_id: Optional[UUID] = None


class EmployeeLogic:
    @staticmethod
    def all(page: int, location_filter: Optional[UUID] = None, search: Optional[str] = None) -> Paginator:
        employees = Employee.all()

        if location_filter:
            employees = filter(lambda employee: employee.location_id == location_filter, employees)

        def check_match(employee: Employee):
            return search in str(employee.ssn)

        if search:
            employees = filter(check_match, employees)

        employee_items = [
            EmployeeItem(
                employee_id=employee.employee_id, name=employee.name, ssn=employee.ssn, phone=employee.work_phone
            )
            for employee in employees
        ]

        return Paginator.paginate(employee_items, page)

    @staticmethod
    def filter(page: int = 1, location_filter: UUID = None) -> Paginator:
        employees = Employee.all()

        filtered_list = [
            EmployeeItem(
                employee_id=employee.employee_id, name=employee.name, ssn=employee.ssn, phone=employee.work_phone
            )
            for employee in employees
            if location_filter is not None and employee.location_id == location_filter
        ]

        return Paginator.paginate(filtered_list, page)

    @staticmethod
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
