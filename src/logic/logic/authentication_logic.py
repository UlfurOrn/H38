from database.models.employee_model import Employee
from utils.authentication import AuthManager


class Verification:
    @staticmethod
    def login(ssn: int) -> None:
        """Check if a user exists with this SSN. If not, raise an error otherwise
        use AuthManger to set logged_in_user to the user found
        """
        employees = Employee.all()
        for employee in employees:
            if employee.ssn == ssn:
                AuthManager.logged_in_user = employee.id
                return

        raise Exception("User not found in database")

    @staticmethod
    def check_supervisor():
        """Should fetch user with ID AuthManager.logged_in_user_id and raise exception
        if not a supervisor
        """
        user_id = AuthManager.logged_in_user
        user = Employee.get(user_id)
        if not user.is_supervisor:
            raise Exception("User is not a supervisor")
