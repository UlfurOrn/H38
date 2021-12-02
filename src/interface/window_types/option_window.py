from enum import Enum
from typing import Any

from interface.window_types.list_window import EmployeeListWindow, LocationListWindow
from interface.window_types.window import Button, Window


class OptionWindow(Window):
    options: list

    def display(self) -> None:
        self.boundary()
        self.empty()
        for index, option in enumerate(self.options, start=1):
            self.padded(f"{index}: {option}")
        self.empty()
        self.boundary()

    def parse_input(self, data: str) -> None:
        if not data.isdigit():
            raise Exception("Invalid Input: Input must be a valid integer")

        index = int(data) - 1
        if index not in range(len(self.options)):
            raise Exception("Invalid Input: Input must be a valid option")

        self.window_specific(self.options[index])

    def window_specific(self, data: Any) -> Any:
        raise NotImplementedError()


class MainMenuOptions(str, Enum):
    Employees = "Employees"
    Locations = "Locations"
    Contractors = "Contractors"
    Requests = "Requests"
    Reports = "Reports"


class MainMenu(OptionWindow):
    title = "Main Menu"
    options = list(MainMenuOptions)
    buttons = [Button(letter="b", description="back", function=None)]

    def window_specific(self, option: MainMenuOptions) -> Any:
        options = {MainMenuOptions.Employees: EmployeeListWindow(), MainMenuOptions.Locations: LocationListWindow()}

        if option not in options:
            raise Exception(f"Add option for: {option}")

        window = options[option]
        window.run()
