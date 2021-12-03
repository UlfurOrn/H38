from enum import Enum
from typing import Any, Optional
from uuid import UUID

from interface.extra import BACK, Column, Field
from interface.window_types.create_window import CreateWindow
from interface.window_types.list_window import ListWindow
from interface.window_types.option_window import OptionWindow
from interface.window_types.update_window import UpdateWindow
from interface.window_types.view_window import ViewWindow
from logic.api import api
from logic.logic.employee_logic import EmployeeCreate, EmployeeInfo, EmployeeItem, EmployeeUpdate
from logic.logic.location_logic import LocationInfo, LocationItem


class MainMenuOptions(str, Enum):
    Employees = "Employees"
    Locations = "Locations"
    Contractors = "Contractors"
    Requests = "Requests"
    Reports = "Reports"


class MainMenu(OptionWindow):
    title = "Main Menu"
    options = list(MainMenuOptions)

    def window_specific(self, option: MainMenuOptions) -> Any:
        options = {MainMenuOptions.Employees: EmployeeListWindow(), MainMenuOptions.Locations: LocationListWindow()}

        if option not in options:
            raise Exception(f"Add option for: {option}")

        window = options[option]
        window.run()


class EmployeeListWindow(ListWindow):
    title = "Employee List"
    columns = [
        Column(name="#", field="", size=3),
        Column(name="Name", field="name", size=21),
        Column(name="SSN", field="ssn", size=12),
        Column(name="Phone", field="phone", size=9),
    ]

    def setup(self) -> None:
        self.paginator = api.employees.all(self.page)

    def view_item(self, item: EmployeeItem) -> None:
        window = EmployeeViewWindow()
        window.model_id = item.employee_id
        window.run()

    def create(self) -> None:
        value = EmployeeCreateWindow().run()
        if value == BACK:
            return

        window = EmployeeViewWindow()
        window.model_id = value
        window.run()


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

    def update(self) -> UUID:
        window = EmployeeUpdateWindow()
        window.model_id = self.model_id
        window.run()

        self.window_setup()


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
        value = LocationListWindow().run()
        if value == BACK:
            return

        self.info["location"] = value.airport
        self.info["location_id"] = value.location_id


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
        super().window_setup()
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


class LocationListWindow(ListWindow):
    title = "Location List"
    columns = [
        Column(name="#", field="", size=3),
        Column(name="Country", field="country", size=15),
        Column(name="Airport", field="airport", size=28),
    ]

    def setup(self) -> None:
        self.paginator = api.locations.all(self.page)

    def view_item(self, item: LocationItem) -> Optional[LocationInfo]:
        window = LocationViewWindow()
        window.model_id = item.location_id
        value = window.run()
        if value == BACK:
            return

        return value


class LocationViewWindow(ViewWindow):
    title = "View Location"
    info: LocationInfo
    fields = [
        Field(name="Country", field="country"),
        Field(name="Airport", field="airport"),
        Field(name="Supervisor", field="supervisor"),
    ]

    def window_setup(self) -> None:
        self.info = api.locations.get(self.model_id)

    def update(self) -> None:
        print("Update")

    def select(self) -> LocationInfo:
        return self.info

    def view(self) -> None:
        print("View")
