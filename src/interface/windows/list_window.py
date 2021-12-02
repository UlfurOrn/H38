from pydantic import BaseModel

from interface.windows.create_window import EmployeeCreateWindow
from interface.windows.view_window import EmployeeViewWindow
from interface.windows.window import Button, Window
from logic.helpers import ListItem, Paginator
from logic.logic.employee_logic import EmployeeItem
from logic.logic_api import api


class Column(BaseModel):
    name: str
    field: str
    size: int


class ListWindow(Window):
    columns: list
    paginator: Paginator
    page: int = 1

    def window_setup(self) -> None:
        assert sum(column.size for column in self.columns) + len(self.columns) + 1 == self.WINDOW_SIZE

    def setup(self) -> None:
        raise NotImplementedError()

    def parse_input(self, data: str) -> None:
        if data == "a" and self.page > 1:
            self.page -= 1
        if data == "d" and self.page < self.paginator.max_page:
            self.page += 1

        if data.isdigit():
            index = int(data)
            items = self.paginator.items
            if index in range(len(items)):
                self.view_item(items[index])

    def view_item(self, item: ListItem) -> None:
        raise NotImplementedError()

    def display(self) -> None:
        self.list_boundary()
        self.list_header()
        self.list_boundary()
        self.list_items()
        self.list_boundary()
        self.list_paginator()
        self.boundary()

    def list_boundary(self) -> None:
        string = "+"
        for column in self.columns:
            string += "-" * column.size
            string += "+"

        print(string)

    def list_header(self) -> None:
        string = "|"
        for column in self.columns:
            string += column.name.center(column.size)
            string += "|"

        print(string)

    def list_items(self) -> None:
        for index, item in enumerate(self.paginator.items):
            string = f"| {index} |"
            for column in self.columns[1:]:
                string += " "
                value = item.get(column.field)
                if len(value) > column.size - 2:
                    value = value[0 : column.size - 2]  # noqa: E203
                value += " " * (column.size - len(value) - 2)
                string += value
                string += " "
                string += "|"

            print(string)

    def list_paginator(self) -> None:
        page = self.paginator.page
        max_page = self.paginator.max_page
        total = self.paginator.total

        print(f"| a: prev   page: {page:>03}/{max_page:>03}  total: {total:>04}   d: next |")


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
        EmployeeCreateWindow().run()

    buttons = [
        Button(letter="c", description="create", function=create),
        Button(letter="b", description="back", function=None),
    ]


class LocationListWindow(ListWindow):
    title = "Location List"
    columns = [
        Column(name="#", field="", size=3),
        Column(name="Country", field="country", size=15),
        Column(name="Airport", field="airport", size=28),
    ]
    buttons = [Button(letter="b", description="back", function=None)]

    def setup(self) -> None:
        self.paginator = api.locations.all(self.page)

    def view_item(self, item: ListItem) -> None:
        raise NotImplementedError()
