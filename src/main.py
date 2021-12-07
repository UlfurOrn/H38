from uuid import UUID, uuid4
from logic.logic.report_logic import ReportCreate
from logic.logic.employee_logic import EmployeeCreate
from logic.logic.contractor_logic import ContractorCreate

from database.models.employee_model import Employee
from interface.windows import MainMenu
from utils.authentication import AuthManager

if __name__ == "__main__":
    """EmployeeCreate(
        name="Test",
        ssn=1334,
        address="Address",
        home_phone=None,
        work_phone=13432,
        email="email",
        location_id=uuid4()
    )"""

    """ContractorCreate(
        name = "Test",
        phone=24213,
        email="email@email.com",
        opening_hours= "08:15 - 21:50",
        location_id=uuid4()
    )"""

    ReportCreate(
        property_id=uuid4(),
        employee_id=uuid4(),
        description="Bla bla",
        cost="test",
        status= "test",
        date= "4/1/2001",
        contractor_id=uuid4(),
    )

    # user = Employee.get(UUID("991f4dc9-b293-409d-aaac-68467aecfc2e"))
   #  AuthManager.set_user(user)
    # MainMenu().run()
