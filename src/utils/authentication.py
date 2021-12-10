from typing import Optional
from uuid import UUID

from database.models.employee_model import Employee
from utils.exceptions import ForbiddenException


class AuthManager:
    __logged_in_user_id: Optional[UUID] = None

    @classmethod
    def get_user(cls) -> Employee:
        if cls.__logged_in_user_id is not None:
            return Employee.get(cls.__logged_in_user_id)

    @classmethod
    def set_user(cls, user: Employee) -> None:
        cls.__logged_in_user_id = user.id


def requires_supervisor(function):
    def wrapper(*args, **kwargs):
        user = AuthManager.get_user()
        if not user.is_supervisor():
            raise ForbiddenException("User is not a supervisor")

        return function(*args, **kwargs)

    return wrapper
