from pydantic import BaseModel

from interface.windows.window import Window
from logic.helpers import Paginator
from logic.logic_api import api


class Column(BaseModel):
    name: str
    field: str
    size: int


class ListWindow(Window):
    columns: list
    paginator: Paginator
    page: int = 1

    def run(self):
        assert sum(column.size for column in self.columns) + len(self.columns) + 1 == self.WINDOW_SIZE

        while True:
            self.setup()
            self.display()
            data = self.get_input()
            if data == "b":
                return

            if data == "a" and self.page > 1:
                self.page -= 1
            if data == "d" and self.page < self.paginator.max_page:
                self.page += 1

    def setup(self) -> None:
        pass

    def list_boundary(self) -> None:
        boundary = list(self._get_boundary())

        index = 0
        for column in self.columns:
            index += column.size + 1
            boundary[index] = "+"

        boundary = "".join(boundary)
        print(boundary)

    def list_header(self) -> None:
        string = "|"
        for column in self.columns:
            column_name = column.name
            string += column_name.center(column.size)
            string += "|"

        print(string)

    def list_items(self) -> None:
        for item in self.paginator.items:
            string = "|"
            for column in self.columns:
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

    def display(self) -> None:
        self.boundary()
        self.title("Employee List")
        self.list_boundary()
        self.list_header()
        self.list_boundary()
        self.list_items()
        self.list_boundary()
        self.list_paginator()
        self.boundary()
        print()


class EmployeeList(ListWindow):
    columns = [
        Column(name="Name", field="name", size=26),
        Column(name="SSN", field="ssn", size=11),
        Column(name="Phone", field="phone", size=9),
    ]

    def setup(self) -> None:
        self.paginator = api.employees.all(self.page)
