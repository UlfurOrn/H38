from uuid import UUID
from Verklegt_1.H38.src.database.models.employee_model import Employee
from utils.authentication_manager import AuthManager
from database.models import *


class Verification:
    def login(ssn: int) -> None:
        """Check if a user exists with this SSN. If not, raise an error otherwise
        use AuthManger to set logged_in_user to the user found
        """
        employees = Employee.all()
        verify = False
        for employee in employees:
            if employee.ssn == ssn:
                user = Employee.get(ssn)
                AuthManager.logged_in_user = user.id
                verify = True
                break
            else:
                pass

        if verify == True:
            pass
        else:
            raise Exception("User not found in database")
        
    def check_supervisor():
        """Should fetch user with ID AuthManager.logged_in_user_id and raise exception
        if not a supervisor
        """
        user = AuthManager.logged_in_user
        if user.is_supervisor == False:
            raise Exception("User is not a supervisor")
        else:
            pass