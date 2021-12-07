from database.models.employee_model import Employee
from utils.authentication import AuthManager
from utils.exceptions import NotFoundException


class AuthenticationLogic:
    @staticmethod
    def login(ssn: int) -> None:
        employees = Employee.all()
        for employee in employees:
            if employee.ssn == ssn:
                AuthManager.set_user(employee)
                return

        raise NotFoundException(f'User with SSN "{ssn}" not found')

    @staticmethod
    def is_supervisor():
        user = AuthManager.get_user()
        return user.is_supervisor()
