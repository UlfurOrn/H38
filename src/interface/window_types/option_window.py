from enum import Enum
from typing import Any, Type

from interface.window_types.window import Button, Window


class OptionWindow(Window):
    options: list

    def button_setup(self) -> None:
        self.buttons = [Button(letter="b", description="back", function=self.back)]

    def display(self) -> None:
        self.boundary()
        self.empty()
        for index, option in enumerate(self.options, start=1):
            self.padded(f"{index}: {option}")
        self.empty()
        self.boundary()

    def parse_input(self, data: str) -> None:
        if not data.isdigit():
            return

        index = int(data) - 1
        if index not in range(len(self.options)):
            return

        return self.window_specific(self.options[index])

    def window_specific(self, data: Any) -> Any:
        raise NotImplementedError()


class SelectOptionWindow(OptionWindow):
    def __init__(self, options: Type[Enum], title: str = "Choose Option to View"):
        self.title = title
        self.options = list(options)

    def window_specific(self, data: Enum) -> Enum:
        return data
