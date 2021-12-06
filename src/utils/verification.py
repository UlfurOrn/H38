from src.database.models.employee_model import Employee
from utils.authentication import AuthManager


class Verification:
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
        
    def check_supervisor():
        """Should fetch user with ID AuthManager.logged_in_user_id and raise exception
        if not a supervisor
        """
        user_id = AuthManager.logged_in_user
        user = Employee.get(user_id)
        if not user.is_supervisor:
            raise Exception("User is not a supervisor")

    def supervisor_verify():
        """Checks if the user is a supervisor and returns True if he is, 
        false otherwise"""
        user_id = AuthManager.logged_in_user
        user = Employee.get(user_id)
        if not user.is_supervisor:
            return False
        else: 
            return True