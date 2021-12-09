from typing import Optional
from interface.extra import WindowState

from interface.extra import Button
from interface.window_types.window import Window
from logic.helpers import InfoModel, ListItem, Paginator


class ListWindow(Window):
    columns: list
    paginator: Paginator
    page: int = 1

    def __init__(self, window_state: WindowState) -> None:
        super().__init__()
        self.window_state = window_state

    def button_setup(self) -> None:
        self.buttons = [
            Button(letter="c", description="create", function=self.create, supervisor=True),
            Button(letter="f", description="filter", function=self.filter),
            Button(letter="s", description="search", function=self.search),
            Button(letter="b", description="back", function=self.back),
        ]

    def window_setup(self) -> None:
        assert sum(column.size for column in self.columns) + len(self.columns) + 1 == self.WINDOW_SIZE
    
    def hide_buttons(self) -> None:
        if self.window_state == WindowState.Normal:
            self.hide_button("a")
            self.hide_button("s")
        elif self.window_state == WindowState.Add:
            self.hide_button("c")
        elif self.window_state == WindowState.Select:
            self.hide_button("c")
            self.hide_button("a")
        elif self.window_state == WindowState.View:
            self.hide_button("a")
            self.hide_button("s")
            self.hide_button("c")

    def setup(self) -> None:
        raise NotImplementedError()

    def parse_input(self, data: str) -> None:
        if data == "a" and self.page > 1:
            self.page -= 1
        if data == "d" and self.page < self.paginator.max_page:
            self.page += 1

        if data.isdigit():
            index = int(data) - 1
            if index < 0:
                index += 10
            items = self.paginator.items
            if index in range(len(items)):
                return self.view_item(items[index])

    def view_item(self, item: ListItem) -> Optional[InfoModel]:
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

    def create(self) -> None:
        raise NotImplementedError()

    def filter(self) -> None:
        raise NotImplementedError()

    def search(self) -> None:
        raise NotImplementedError()
