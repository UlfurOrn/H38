from enum import Enum
from typing import Any, Optional, Union
from uuid import UUID

from database.models.property_model import Condition
from interface.extra import BACK, Column, Field
from interface.window_types.create_window import CreateWindow
from interface.window_types.list_window import ListWindow
from interface.window_types.option_window import OptionWindow
from interface.window_types.update_window import UpdateWindow
from interface.window_types.view_window import ViewWindow
from logic.api import api
from logic.logic.employee_logic import EmployeeCreate, EmployeeInfo, EmployeeItem, EmployeeUpdate
from logic.logic.location_logic import LocationCreate, LocationInfo, LocationItem, LocationUpdate
from logic.logic.property_logic import PropertyCreate, PropertyInfo, PropertyItem


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

    def setup(self) -> None:
        self.paginator = api.employees.all(self.page)

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


###############################################################################


# Location Windows:
###############################################################################
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
        value = LocationViewWindow(item.location_id).run()
        if value == BACK:
            return
        return value

    def create(self) -> None:
        value = LocationCreateWindow().run()
        if value == BACK:
            return

        LocationViewWindow(value).run()


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
        print("View")


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
        employee_id = api.locations.update(self.model_id, data)

        return employee_id

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


###############################################################################


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

    def select(self) -> PropertyInfo:
        return self.info

    def view(self) -> None:
        value: Union[BACK, PropertyViewOptions] = PropertyViewOptionsWindow().run()
        if value == BACK:
            return

        if value == PropertyViewOptions.Location:
            LocationViewWindow(self.info.location_id).run()

        if value == PropertyViewOptions.Facilities:
            FacilityListWindow(property_id=self.info.property_id).run()


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
            value: Union[BACK, Condition] = ChooseConditionWindow().run()
            if value == BACK:
                return

            self.info["condition"] = value.value

    def clear(self) -> None:
        super().clear()
        field = self.fields[self.current]
        if field.field == "location":
            self.info["location_id"] = None


class PropertyViewOptions(str, Enum):
    Location = "Location"
    Facilities = "Facilities"


class PropertyViewOptionsWindow(OptionWindow):
    title = "Choose Option to View"
    options = list(PropertyViewOptions)

    def window_specific(self, data: PropertyViewOptions) -> PropertyViewOptions:
        return data


###############################################################################


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

    # def view_item(self, item: PropertyItem) -> None:
    #     window = PropertyViewWindow()
    #     window.model_id = item.property_id
    #     value = window.run()
    #     if value == BACK:
    #         return
    #
    #     return value
    #
    # def create(self) -> None:
    #     value = PropertyCreateWindow().run()
    #     if value == BACK:
    #         return
    #
    #     window = PropertyViewWindow()
    #     window.model_id = value
    #     window.run()


###############################################################################


# Extra Windows:
###############################################################################
class ChooseConditionWindow(OptionWindow):
    title = "Choose Condition"
    options = list(Condition)

    def window_specific(self, data: Condition) -> Condition:
        return data
