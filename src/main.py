from uuid import UUID, uuid4
from interface.windows import Welcome
from logic.logic.report_logic import ReportCreate
from logic.logic.employee_logic import EmployeeCreate
from logic.logic.contractor_logic import ContractorCreate

from database.models.employee_model import Employee
from interface.windows import MainMenu
from utils.authentication import AuthManager

if __name__ == "__main__":
    Welcome().run()
