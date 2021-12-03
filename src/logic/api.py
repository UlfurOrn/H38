from logic.logic.employee_logic import EmployeeLogic
from logic.logic.location_logic import LocationLogic


class LogicAPI:
    employees = EmployeeLogic
    locations = LocationLogic


api = LogicAPI
