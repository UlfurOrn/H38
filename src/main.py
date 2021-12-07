from uuid import UUID

from database.models.employee_model import Employee
from interface.windows import MainMenu
from utils.authentication import AuthManager

if __name__ == "__main__":
    user = Employee.get(UUID("e42cee48-1424-45a3-95a6-3d6037a57d5f"))
    AuthManager.set_user(user)
    MainMenu().run()
