from src.database.models.employee_model import Employee
from utils.authentication import AuthManager


class AuthenticationLogic:
    @staticmethod
    def login(ssn: int) -> None:
        employees = Employee.all()
        for employee in employees:
            if employee.ssn == ssn:
                AuthManager.set_user(employee)
                return

        raise Exception("User not found in database")

    @staticmethod
    def is_supervisor():
        user = AuthManager.get_user()
        return user.is_supervisor()
