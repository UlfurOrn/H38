from uuid import UUID

from database.models.employee_model import Employee
from interface.windows import MainMenu
from utils.authentication import AuthManager

if __name__ == "__main__":
    user = Employee.get(UUID("991f4dc9-b293-409d-aaac-68467aecfc2e"))
    AuthManager.set_user(user)
    MainMenu().run()
