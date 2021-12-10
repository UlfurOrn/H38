from datetime import date, datetime
from enum import Enum
from typing import Any, Optional, Union
from uuid import UUID

from database.models.property_model import Condition
from database.models.report_model import ReportStatus
from database.models.request_model import Priority, RequestStatus
from interface.extra import BACK, Button, Column, Field
from interface.window_types.create_window import CreateWindow
from interface.window_types.filter_window import FilterWindow
from interface.window_types.list_window import ListWindow
from interface.window_types.option_window import OptionWindow, SelectOptionWindow
from interface.window_types.update_window import UpdateWindow
from interface.window_types.view_window import ViewWindow
from interface.window_types.window import Window
from logic.api import api
from logic.logic.contractor_logic import ContractorCreate, ContractorInfo, ContractorItem, ContractorUpdate
from logic.logic.employee_logic import EmployeeCreate, EmployeeFilterOptions, EmployeeInfo, EmployeeItem, EmployeeUpdate
from logic.logic.facility_logic import FacilityCreate, FacilityInfo, FacilityItem, FacilityUpdate
from logic.logic.location_logic import LocationCreate, LocationFilterOptions, LocationInfo, LocationItem, LocationUpdate
from logic.logic.property_logic import PropertyCreate, PropertyInfo, PropertyItem, PropertyUpdate
from logic.logic.report_logic import ReportCreate, ReportInfo, ReportItem
from logic.logic.request_logic import (
    MultipleRequestCreate,
    RequestInfo,
    RequestItem,
    RequestUpdate,
    SingleRequestCreate,
)
from utils.authentication import AuthManager
from utils.exceptions import BadRequestException


class MainMenuOptions(str, Enum):
    Employees = "Employees"
    Locations = "Locations"
    Properties = "Properties"
    Contractors = "Contractors"
    Requests = "Requests"
    Reports = "Reports"


class MainMenu(OptionWindow):
    title = "Main Menu"
    options = list(MainMenuOptions)

    def window_specific(self, option: MainMenuOptions) -> Any:
        options = {
            MainMenuOptions.Employees: EmployeeListWindow(),
            MainMenuOptions.Locations: LocationListWindow(),
            MainMenuOptions.Properties: PropertyListWindow(),
            MainMenuOptions.Contractors: ContractorListWindow(),
            MainMenuOptions.Requests: RequestListWindow(),
            MainMenuOptions.Reports: ReportListWindow(),
        }

        if option not in options:
            raise Exception(f"Add option for: {option}")

        window = options[option]
        window.run()


# Employee Windows:
###############################################################################
class EmployeeListWindow(ListWindow):
    title = "Employee List"
    columns = [
        Column(name="#", field="", size=3),
        Column(name="Name", field="name", size=21),
        Column(name="SSN", field="ssn", size=12),
        Column(name="Phone", field="phone", size=9),
    ]
    filters = EmployeeFilterOptions()

    def setup(self) -> None:
        self.paginator = api.employees.all(self.page, self.filters)

    def view_item(self, item: EmployeeItem) -> None:
        value = EmployeeViewWindow(item.employee_id).run()
        if value == BACK:
            return
        return value

    def create(self) -> None:
        value = EmployeeCreateWindow().run()
        if value == BACK:
            return

        EmployeeViewWindow(value).run()

    def filter(self) -> None:
        value = EmployeeFilterWindow(self.filters).run()
        if value == BACK:
            return
        self.filters = value
        self.page = 1


class EmployeeViewWindow(ViewWindow):
    title = "View Employee"
    info: EmployeeInfo
    fields = [
        Field(name="Name", field="name"),
        Field(name="SSN", field="ssn"),
        Field(name="Address", field="address"),
        Field(name="Email", field="email"),
        Field(name="Home Phone", field="home_phone"),
        Field(name="Work Phone", field="work_phone"),
        Field(name="Location", field="location"),
    ]

    def window_setup(self) -> None:
        self.info = api.employees.get(self.model_id)

    def update(self) -> None:
        EmployeeUpdateWindow(self.model_id).run()
        self.window_setup()

    def select(self) -> EmployeeInfo:
        return self.info

    def view(self) -> None:
        value: Union[BACK, EmployeeViewOptions] = SelectOptionWindow(EmployeeViewOptions).run()
        if value == BACK:
            return

        if value == EmployeeViewOptions.Location:
            LocationViewWindow(self.info.location_id).run()


class EmployeeCreateWindow(CreateWindow):
    title = "Create Employee"
    fields = [
        Field(name="Name", field="name"),
        Field(name="SSN", field="ssn", mutable=False),
        Field(name="Address", field="address"),
        Field(name="Email", field="email"),
        Field(name="Home Phone", field="home_phone", required=False),
        Field(name="Work Phone", field="work_phone"),
        Field(name="Location", field="location", submenu=True),
    ]

    def submit(self) -> UUID:
        data = EmployeeCreate(**self.info)
        employee_id = api.employees.create(data)

        return employee_id

    def submenu(self) -> None:
        value: Union[BACK, LocationInfo] = LocationListWindow().run()
        if value == BACK:
            return

        self.info["location"] = value.airport
        self.info["location_id"] = value.location_id

    def clear(self) -> None:
        super().clear()
        field = self.fields[self.current]
        if field.field == "location":
            self.info["location_id"] = None


class EmployeeUpdateWindow(UpdateWindow):
    title = "Update Employee"
    fields = [
        Field(name="Name", field="name"),
        Field(name="SSN", field="ssn", mutable=False),
        Field(name="Address", field="address"),
        Field(name="Email", field="email"),
        Field(name="Home Phone", field="home_phone", required=False),
        Field(name="Work Phone", field="work_phone"),
        Field(name="Location", field="location", submenu=True),
    ]

    def window_setup(self) -> None:
        self.info = api.employees.get(self.model_id).dict()

    def submit(self) -> UUID:
        data = EmployeeUpdate(**self.info)
        employee_id = api.employees.update(self.model_id, data)

        return employee_id

    def submenu(self) -> None:
        value = LocationListWindow().run()
        if value == BACK:
            return

        self.info["location"] = value.airport
        self.info["location_id"] = value.location_id

    def clear(self) -> None:
        super().clear()
        field = self.fields[self.current]
        if field.field == "location":
            self.info["location_id"] = None


class EmployeeViewOptions(str, Enum):
    Location = "Location"


class EmployeeFilterWindow(FilterWindow):
    title = "Employee Filters"
    fields = [
        Field(name="Location", field="location", submenu=True),
        Field(name="SSN", field="ssn"),
        Field(name="Name", field="name"),
        Field(name="Phone", field="phone"),
    ]

    def save(self) -> EmployeeFilterOptions:
        return EmployeeFilterOptions(**self.info)

    def submenu(self) -> None:
        value: Union[BACK, LocationInfo] = LocationListWindow().run()
        if value == BACK:
            return
        self.info["location"] = value.airport
        self.info["location_id"] = value.location_id

    def clear(self) -> None:
        super().clear()
        self.info["location_id"] = None


# Location Windows:
###############################################################################
class LocationListWindow(ListWindow):
    title = "Location List"
    columns = [
        Column(name="#", field="", size=3),
        Column(name="Country", field="country", size=15),
        Column(name="Airport", field="airport", size=28),
    ]
    filters = LocationFilterOptions()

    def setup(self) -> None:
        self.paginator = api.locations.all(self.page, self.filters)

    def view_item(self, item: LocationItem) -> Optional[LocationInfo]:
        value = LocationViewWindow(item.location_id).run()
        if value == BACK:
            return
        return value

    def create(self) -> None:
        value = LocationCreateWindow().run()
        if value == BACK:
            return

        LocationViewWindow(value).run()

    def filter(self) -> None:
        value = LocationFilterWindow(self.filters).run()
        if value == BACK:
            return
        self.filters = value
        self.page = 1


class LocationViewWindow(ViewWindow):
    title = "View Location"
    info: LocationInfo
    fields = [
        Field(name="Country", field="country"),
        Field(name="Airport", field="airport"),
        Field(name="Phone", field="phone"),
        Field(name="Opening Hours", field="opening_hours"),
        Field(name="Supervisor", field="supervisor"),
    ]

    def window_setup(self) -> None:
        self.info = api.locations.get(self.model_id)

    def update(self) -> None:
        LocationUpdateWindow(self.model_id).run()
        self.window_setup()

    def select(self) -> LocationInfo:
        return self.info

    def view(self) -> None:
        value: Union[BACK, LocationViewOptions] = SelectOptionWindow(LocationViewOptions).run()
        if value == BACK:
            return

        if value == LocationViewOptions.Supervisor:
            EmployeeViewWindow(self.info.supervisor_id).run()


class LocationCreateWindow(CreateWindow):
    title = "Create Location"
    fields = [
        Field(name="Country", field="country", mutable=False),
        Field(name="Airport", field="airport"),
        Field(name="Phone", field="phone"),
        Field(name="Opening Hours", field="opening_hours"),
        Field(name="Supervisor", field="supervisor", required=False, submenu=True),
    ]

    def submit(self) -> UUID:
        data = LocationCreate(**self.info)
        location_id = api.locations.create(data)

        return location_id

    def submenu(self) -> None:
        value: Union[BACK, EmployeeInfo] = EmployeeListWindow().run()
        if value == BACK:
            return

        self.info["supervisor"] = value.name
        self.info["supervisor_id"] = value.employee_id

    def clear(self) -> None:
        super().clear()
        field = self.fields[self.current]
        if field.field == "supervisor":
            self.info["supervisor_id"] = None


class LocationUpdateWindow(UpdateWindow):
    title = "Update Location"
    fields = [
        Field(name="Country", field="country", mutable=False),
        Field(name="Airport", field="airport"),
        Field(name="Phone", field="phone"),
        Field(name="Opening Hours", field="opening_hours"),
        Field(name="Supervisor", field="supervisor", required=False, submenu=True),
    ]

    def window_setup(self) -> None:
        self.info = api.locations.get(self.model_id).dict()

    def submit(self) -> UUID:
        data = LocationUpdate(**self.info)
        location_id = api.locations.update(self.model_id, data)

        return location_id

    def submenu(self) -> None:
        value: Union[BACK, EmployeeInfo] = EmployeeListWindow().run()
        if value == BACK:
            return

        self.info["supervisor"] = value.name
        self.info["supervisor_id"] = value.employee_id

    def clear(self) -> None:
        super().clear()
        field = self.fields[self.current]
        if field.field == "location":
            self.info["location_id"] = None


class LocationViewOptions(str, Enum):
    Supervisor = "Supervisor"


class LocationFilterWindow(FilterWindow):
    title = "Location Filters"
    fields = [
        Field(name="Country", field="country"),
        Field(name="Airport", field="airport"),
        Field(name="Phone", field="phone"),
    ]

    def save(self) -> LocationFilterOptions:
        return LocationFilterOptions(**self.info)

    def submenu(self) -> None:
        pass


# Property Windows:
###############################################################################
class PropertyListWindow(ListWindow):
    title = "Property List"
    columns = [
        Column(name="#", field="", size=3),
        Column(name="Property Number", field="property_number", size=17),
        Column(name="Location", field="location", size=14),
        Column(name="Condition", field="condition", size=11),
    ]

    def setup(self) -> None:
        self.paginator = api.properties.all(self.page)

    def view_item(self, item: PropertyItem) -> None:
        value = PropertyViewWindow(item.property_id).run()
        if value == BACK:
            return

        return value

    def create(self) -> None:
        value: Union[BACK, UUID] = PropertyCreateWindow().run()
        if value == BACK:
            return

        PropertyViewWindow(value).run()


class PropertyViewWindow(ViewWindow):
    title = "View Property"
    info: PropertyInfo
    fields = [
        Field(name="Property Number", field="property_number"),
        Field(name="Area (m^2)", field="area"),
        Field(name="Location", field="location"),
        Field(name="Condition", field="condition"),
        Field(name="Facilities", field="facilities"),
    ]

    def window_setup(self) -> None:
        self.info = api.properties.get(self.model_id)

    def update(self) -> None:
        PropertyUpdateWindow(self.model_id).run()
        self.window_setup()

    def select(self) -> PropertyInfo:
        return self.info

    def view(self) -> None:
        value: Union[BACK, PropertyViewOptions] = SelectOptionWindow(PropertyViewOptions).run()
        if value == BACK:
            return

        if value == PropertyViewOptions.Location:
            LocationViewWindow(self.info.location_id).run()

        if value == PropertyViewOptions.Facilities:
            FacilityListWindow(property_id=self.info.property_id).run()
            self.window_setup()


class PropertyCreateWindow(CreateWindow):
    title = "Create Property"
    fields = [
        Field(name="Property Number", field="property_number"),
        Field(name="Area (m^2)", field="area"),
        Field(name="Location", field="location", submenu=True),
        Field(name="Condition", field="condition", submenu=True),
    ]

    def submit(self) -> UUID:
        data = PropertyCreate(**self.info)
        property_id = api.properties.create(data)

        return property_id

    def submenu(self) -> None:
        field = self.fields[self.current]
        if field.field == "location":
            value: Union[BACK, LocationInfo] = LocationListWindow().run()
            if value == BACK:
                return

            self.info["location"] = value.airport
            self.info["location_id"] = value.location_id
        else:
            value: Union[BACK, Condition] = SelectOptionWindow(Condition).run()
            if value == BACK:
                return

            self.info["condition"] = value.value

    def clear(self) -> None:
        super().clear()
        field = self.fields[self.current]
        if field.field == "location":
            self.info["location_id"] = None


class PropertyUpdateWindow(UpdateWindow):
    title = "Update Property"
    fields = [
        Field(name="Property Number", field="property_number", mutable=False),
        Field(name="Area (m^2)", field="area"),
        Field(name="Location", field="location", submenu=True, mutable=False),
        Field(name="Condition", field="condition", submenu=True),
    ]

    def window_setup(self) -> None:
        self.info = api.properties.get(self.model_id).dict()

    def submit(self) -> UUID:
        data = PropertyUpdate(**self.info)
        property_id = api.properties.update(self.model_id, data)

        return property_id

    def submenu(self) -> None:
        value: Union[BACK, Condition] = SelectOptionWindow(Condition).run()
        if value == BACK:
            return

        self.info["condition"] = value.value


class PropertyViewOptions(str, Enum):
    Location = "Location"
    Facilities = "Facilities"


# Facility Windows:
###############################################################################
class FacilityListWindow(ListWindow):
    title = "Facility List"
    columns = [
        Column(name="#", field="", size=3),
        Column(name="Name", field="name", size=32),
        Column(name="Condition", field="condition", size=11),
    ]

    def __init__(self, property_id: UUID):
        self.property_id = property_id

    def setup(self) -> None:
        self.paginator = api.facilities.all(self.property_id, self.page)

    def view_item(self, item: FacilityItem) -> None:
        value = FacilityViewWindow(item.facility_id).run()
        if value == BACK:
            return
        return value

    def create(self) -> None:
        value = FacilityCreateWindow(self.property_id).run()
        if value == BACK:
            return

        FacilityViewWindow(value).run()


class FacilityViewWindow(ViewWindow):
    title = "View Facility"
    info: FacilityInfo
    fields = [
        Field(name="Name", field="name"),
        Field(name="Condition", field="condition"),
        Field(name="Property", field="property"),
    ]

    def window_setup(self) -> None:
        self.info = api.facilities.get(self.model_id)

    def update(self) -> None:
        FacilityUpdateWindow(self.model_id).run()
        self.window_setup()

    def select(self) -> FacilityInfo:
        return self.info

    def view(self) -> None:
        pass


class FacilityCreateWindow(CreateWindow):
    title = "Create Facility"
    fields = [Field(name="Name", field="name"), Field(name="Condition", field="condition", submenu=True)]

    def __init__(self, property_id: UUID):
        self.property_id = property_id

    def submit(self) -> UUID:
        data = FacilityCreate(**self.info)
        facility_id = api.facilities.create(self.property_id, data)

        return facility_id

    def submenu(self) -> None:
        value: Union[BACK, Condition] = SelectOptionWindow(Condition, "Select Condition").run()
        if value == BACK:
            return

        self.info["condition"] = value.value


class FacilityUpdateWindow(UpdateWindow):
    title = "Update Facility"
    fields = [Field(name="Name", field="name"), Field(name="Condition", field="condition", submenu=True)]

    def window_setup(self) -> None:
        self.info = api.facilities.get(self.model_id).dict()

    def submit(self) -> UUID:
        data = FacilityUpdate(**self.info)
        property_id = api.facilities.update(self.model_id, data)

        return property_id

    def submenu(self) -> None:
        value: Union[BACK, Condition] = SelectOptionWindow(Condition, "Select Condition").run()
        if value == BACK:
            return

        self.info["condition"] = value.value


# Contractor Windows:
###############################################################################
class ContractorListWindow(ListWindow):
    title = "Contractor List"
    columns = [
        Column(name="#", field="", size=3),
        Column(name="Name", field="name", size=20),
        Column(name="Location", field="location", size=13),
        Column(name="Phone", field="phone", size=9),
    ]

    def setup(self) -> None:
        self.paginator = api.contractors.all(self.page)

    def view_item(self, item: ContractorItem) -> None:
        value = ContractorViewWindow(item.contractor_id).run()
        if value == BACK:
            return
        return value

    def create(self) -> None:
        value = ContractorCreateWindow().run()
        if value == BACK:
            return
        ContractorViewWindow(value).run()


class ContractorViewWindow(ViewWindow):
    title = "View Contractor"
    info: ContractorInfo
    fields = [
        Field(name="Name", field="name"),
        Field(name="Phone", field="phone"),
        Field(name="Email", field="email"),
        Field(name="Opening Hours", field="opening_hours"),
        Field(name="Location", field="location"),
    ]

    def window_setup(self) -> None:
        self.info = api.contractors.get(self.model_id)

    def update(self) -> None:
        ContractorUpdateWindow(self.model_id).run()
        self.window_setup()

    def select(self) -> ContractorInfo:
        return self.info

    def view(self) -> None:
        value: Union[BACK, ContractorViewOptions] = SelectOptionWindow(ContractorViewOptions).run()
        if value == BACK:
            return

        if value == ContractorViewOptions.Location:
            LocationViewWindow(self.info.location_id).run()


class ContractorCreateWindow(CreateWindow):
    title = "Create Contractor"
    fields = [
        Field(name="Name", field="name"),
        Field(name="Phone", field="phone"),
        Field(name="Email", field="email"),
        Field(name="Opening Hours", field="opening_hours"),
        Field(name="Location", field="location", submenu=True),
    ]

    def submit(self) -> UUID:
        data = ContractorCreate(**self.info)
        contractor_id = api.contractors.create(data)

        return contractor_id

    def submenu(self) -> None:
        value: Union[BACK, LocationInfo] = LocationListWindow().run()
        if value == BACK:
            return

        self.info["location"] = value.airport
        self.info["location_id"] = value.location_id


class ContractorUpdateWindow(UpdateWindow):
    title = "Update Contractor"
    fields = [
        Field(name="Name", field="name"),
        Field(name="Phone", field="phone"),
        Field(name="Email", field="email"),
        Field(name="Opening Hours", field="opening_hours"),
        Field(name="Location", field="location", submenu=True),
    ]

    def window_setup(self) -> None:
        self.info = api.contractors.get(self.model_id).dict()

    def submit(self) -> UUID:
        data = ContractorUpdate(**self.info)
        contractor_id = api.contractors.update(self.model_id, data)

        return contractor_id

    def submenu(self) -> None:
        value: Union[BACK, LocationInfo] = LocationListWindow().run()
        if value == BACK:
            return

        self.info["location"] = value.airport
        self.info["location_id"] = value.location_id


class ContractorViewOptions(str, Enum):
    Location = "Location"


# Request Windows:
###############################################################################
class RequestListWindow(ListWindow):
    title = "Request List"
    columns = [
        Column(name="#", field="", size=3),
        Column(name="Property", field="property", size=12),
        Column(name="Date", field="date", size=10),
        Column(name="Priority", field="priority", size=10),
        Column(name="Status", field="status", size=9),
    ]

    def setup(self) -> None:
        self.paginator = api.requests.all(self.page)

    def view_item(self, item: RequestItem) -> None:
        value = RequestViewWindow(item.request_id).run()
        if value == BACK:
            return
        return value

    def create(self) -> None:
        value = RecurringRequestWindow().run()
        if value == BACK:
            return
        RequestViewWindow(value).run()


class RequestContractorsListWindow(ContractorListWindow):
    def __init__(self, request_id: UUID):
        self.request_id = request_id

    def setup(self) -> None:
        self.paginator = api.requests.contractors(self.request_id, self.page)

    def add(self) -> None:
        value: Union[BACK, ContractorInfo] = ContractorListWindow().run()
        if value == BACK:
            return

        api.requests.add_contractor(self.request_id, value.contractor_id)


class RequestViewWindow(ViewWindow):
    title = "View Request"
    info: RequestInfo
    fields = [
        Field(name="Property", field="property", submenu=True),
        Field(name="Date", field="date"),
        Field(name="Priority", field="priority", submenu=True),
        Field(name="Status", field="status", submenu=True),
        Field(name="Employee", field="employee", submenu=True),
        Field(name="Contractors", field="contractors"),
    ]

    def button_setup(self) -> None:
        self.buttons = [
            Button(letter="u", description="update", function=self.update),
            Button(letter="a", description="assign", function=self.assign),
            Button(letter="d", description="done", function=self.done),
            Button(letter="r", description="report", function=self.report),
            Button(letter="s", description="select", function=self.select),
            Button(letter="v", description="view", function=self.view),
            Button(letter="b", description="back", function=self.back),
        ]

    def window_setup(self) -> None:
        self.info = api.requests.get(self.model_id)

    def setup(self) -> None:
        if self.info.status != RequestStatus.Todo:
            self.hide_button("a")
        if self.info.status != RequestStatus.Ongoing:
            self.hide_button("d")
            self.hide_button("u")
        if self.info.status != RequestStatus.Done:
            self.hide_button("c")
            self.hide_button("r")

    def update(self) -> None:
        user = AuthManager.get_user()
        if not (user.is_supervisor() or user.id == self.info.employee_id):
            raise BadRequestException("User is not a supervisor or the assignee")

        RequestUpdateWindow(self.model_id).run()
        self.window_setup()

    def assign(self) -> None:
        api.requests.assign(request_id=self.model_id)
        self.window_setup()

    def done(self) -> None:
        api.requests.done(request_id=self.model_id)
        self.window_setup()

    def report(self) -> None:
        value: Union[BACK, UUID] = ReportCreateWindow(self.info.request_id).run()
        if value == BACK:
            return

        ReportViewWindow(value).run()
        self.window_setup()

    def select(self) -> RequestInfo:
        return self.info

    def view(self) -> None:
        value: Union[BACK, RequestViewOptions] = SelectOptionWindow(RequestViewOptions).run()
        if value == BACK:
            return

        if value == RequestViewOptions.Property:
            PropertyViewWindow(self.info.property_id).run()
        if value == RequestViewOptions.Employee:
            if self.info.employee_id is None:
                raise BadRequestException("No Employee is registered to this task")
            EmployeeViewWindow(self.info.employee_id).run()
        if value == RequestViewOptions.Contractors:
            RequestContractorsListWindow(request_id=self.model_id).run()

        self.window_setup()


class RecurringRequestWindow(Window):
    title = "Create Request"

    def button_setup(self) -> None:
        self.buttons = [
            Button(letter="y", description="yes", function=self.yes),
            Button(letter="n", description="no", function=self.no),
            Button(letter="b", description="back", function=self.back),
        ]

    def display(self) -> None:
        self.boundary()
        self.empty()
        self.centered("Is this a recurring project?")
        self.empty()
        self.boundary()

    @staticmethod
    def yes() -> None:
        return MultipleRequestCreateWindow().run()

    @staticmethod
    def no() -> Union[BACK, UUID]:
        return SingleRequestCreateWindow().run()


class RequestCreateSuperWindow(CreateWindow):
    title = "Create Request"

    def submenu(self) -> None:
        field = self.fields[self.current]
        if field.field == "property":
            value: Union[BACK, PropertyInfo] = PropertyListWindow().run()
            if value == BACK:
                return

            self.info["property"] = value.property_number
            self.info["property_id"] = value.property_id
        if field.field == "priority":
            value: Union[BACK, Priority] = SelectOptionWindow(Priority, "Select Priority").run()
            if value == BACK:
                return

            self.info["priority"] = value.value

    def clear(self) -> None:
        super().clear()
        field = self.fields[self.current]
        if field.field == "property":
            self.info["property_id"] = None


class SingleRequestCreateWindow(RequestCreateSuperWindow):
    fields = [
        Field(name="Property", field="property", submenu=True),
        Field(name="Date", field="date"),
        Field(name="Priority", field="priority", submenu=True),
    ]

    def submit(self) -> UUID:
        data = SingleRequestCreate(**self.info)
        request_id = api.requests.create(data)

        return request_id


class MultipleRequestCreateWindow(RequestCreateSuperWindow):
    fields = [
        Field(name="Property", field="property", submenu=True),
        Field(name="Start Date", field="start_date"),
        Field(name="End Date", field="end_date"),
        Field(name="Interval", field="interval"),
        Field(name="Priority", field="priority", submenu=True),
    ]

    def submit(self) -> UUID:
        data = MultipleRequestCreate(**self.info)
        request_id = api.requests.recurring(data)

        return request_id


class RequestUpdateWindow(UpdateWindow):
    title = "Update Request"
    fields = [
        Field(name="Property", field="property", submenu=True, mutable=False),
        Field(name="Date", field="date"),
        Field(name="Priority", field="priority", submenu=True),
        Field(name="Status", field="status", mutable=False),
        Field(name="Employee", field="employee", mutable=False),
    ]

    def window_setup(self) -> None:
        self.info = api.requests.get(self.model_id).dict()

    def submit(self) -> UUID:
        data = RequestUpdate(**self.info)
        request_id = api.requests.update(self.model_id, data)

        return request_id

    def submenu(self) -> None:
        value: Union[BACK, Priority] = SelectOptionWindow(Priority).run()
        if value == BACK:
            return

        self.info["priority"] = value


class RequestViewOptions(str, Enum):
    Property = "Property"
    Employee = "Employee"
    Contractors = "Contractors"


# Report Windows:
###############################################################################
class ReportListWindow(ListWindow):
    title = "Report List"
    columns = [
        Column(name="#", field="", size=3),
        Column(name="Property", field="property", size=12),
        Column(name="Employee", field="employee", size=18),
        Column(name="Status", field="status", size=12),
    ]

    def setup(self) -> None:
        self.paginator = api.reports.all(self.page)
        self.hide_button("c")  # Create is never used for this window

    def view_item(self, item: ReportItem) -> None:
        value = ReportViewWindow(item.report_id).run()
        if value == BACK:
            return
        return value

    def create(self) -> None:
        pass


class ReportViewWindow(ViewWindow):
    title = "View Report"
    info: ReportInfo
    fields = [
        Field(name="Property", field="property"),
        Field(name="Employee", field="employee"),
        Field(name="Description", field="description"),
        Field(name="Cost", field="cost"),
        Field(name="Contractors", field="contractors"),
        Field(name="Status", field="status"),
    ]

    def button_setup(self) -> None:
        self.buttons = [
            Button(letter="a", description="approve", function=self.approve, supervisor=True),
            Button(letter="u", description="unapprove", function=self.unapprove, supervisor=True),
            Button(letter="c", description="close", function=self.close, supervisor=True),
            Button(letter="c", description="cancel", function=self.cancel, supervisor=True),
            Button(letter="v", description="view", function=self.view),
            Button(letter="b", description="back", function=self.back),
        ]

    def window_setup(self) -> None:
        self.info = api.reports.get(self.model_id)

    def setup(self) -> None:
        if self.info.status != ReportStatus.Unapproved:
            self.hide_button("a")
            self.hide_button("cancel")
        if self.info.status != ReportStatus.Approved:
            self.hide_button("u")
            self.hide_button("close")

    def approve(self) -> None:
        api.reports.approve(self.model_id)
        self.window_setup()

    def unapprove(self) -> None:
        api.reports.unapprove(self.model_id)
        self.window_setup()

    def close(self) -> None:
        api.reports.close(self.model_id)
        self.window_setup()

    def cancel(self) -> None:
        api.reports.cancel(self.model_id)
        self.window_setup()

    def view(self) -> None:
        value: Union[BACK, ReportViewOptions] = SelectOptionWindow(ReportViewOptions).run()
        if value == BACK:
            return

        if value == ReportViewOptions.Request:
            RequestViewWindow(self.info.request_id).run()
        if value == ReportViewOptions.Property:
            PropertyViewWindow(self.info.property_id).run()
        if value == ReportViewOptions.Employee:
            EmployeeViewWindow(self.info.employee_id).run()
        if value == ReportViewOptions.Contractors:
            RequestContractorsListWindow(self.info.request_id).run()


class ReportCreateWindow(CreateWindow):
    title = "Create Report"
    fields = [Field(name="Description", field="description"), Field(name="Cost", field="cost")]

    def __init__(self, request_id: UUID):
        self.request_id = request_id

    def submit(self) -> UUID:
        data = ReportCreate(**self.info)
        report_id = api.reports.create(request_id=self.request_id, data=data)

        return report_id

    def submenu(self) -> None:
        pass


class ReportViewOptions(str, Enum):
    Request = "Request"
    Property = "Property"
    Employee = "Employee"
    Contractors = "Contractors"


# Extra Windows:
###############################################################################
class SelectDateWindow(Window):
    def __init__(self, title: str):
        self.title = title

    def button_setup(self) -> None:
        self.buttons = [Button(letter="b", description="back", function=self.back)]

    def display(self) -> None:
        self.empty()
        self.centered("Enter a date in the following format:")
        self.centered("DD/MM/YY")
        self.empty()

    def parse_input(self, data: str) -> Optional[date]:
        try:
            return datetime.strptime("%d/%m/%Y", data).date()
        except ValueError:
            raise ValueError("Invalid Date Provided: DD/MM/YY")
