from interface.window_types.window import Window
from logic.helpers import ListItem, Paginator


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
            index = (int(data) - 1) % 10
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
            string = f"| {(index + 1) % 10} |"
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
