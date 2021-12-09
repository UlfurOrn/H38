from logic.logic.authentication_logic import AuthenticationLogic
from logic.logic.contractor_logic import ContractorLogic
from logic.logic.employee_logic import EmployeeLogic
from logic.logic.facility_logic import FacilityLogic
from logic.logic.location_logic import LocationLogic
from logic.logic.property_logic import PropertyLogic
from logic.logic.request_logic import RequestLogic


class LogicAPI:
    employees = EmployeeLogic
    locations = LocationLogic
    properties = PropertyLogic
    facilities = FacilityLogic
    contractors = ContractorLogic
    requests = RequestLogic
    authentication = AuthenticationLogic


api = LogicAPI
