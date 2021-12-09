from typing import Any

from interface.extra import BACK, Button
from logic.api import api


class Window:
    WINDOW_SIZE = 50
    title: str
    buttons: list[Button]

    def run(self) -> Any:
        self.button_setup()
        self.window_setup()
        while True:
            self.setup()
            self.display_title()
            self.display()
            self.display_buttons()

            data = self.get_input()
            value = self.parse_data(data)

            if value:
                return value

            self.reset()
            self.clear_screen()

    def button_setup(self) -> None:
        raise NotImplementedError()

    def window_setup(self) -> None:
        pass

    def setup(self) -> None:
        pass

    def display(self) -> None:
        raise NotImplementedError()

    def display_title(self) -> None:
        self.boundary()
        self.centered(self.title)

    def display_buttons(self) -> None:
        user_is_supervisor = api.authentication.is_supervisor()

        buttons = [
            button
            for button in self.buttons
            if not (button.supervisor and not user_is_supervisor) and not button.hidden
        ]

        length_per_button = (self.WINDOW_SIZE - 2) / len(buttons)
        string = "|"

        for button in buttons:
            button_string = f"{button.letter}: {button.description}"
            string += "{:^{}}".format(button_string, round(length_per_button))

        string += "|"
        print(string)

        self.boundary()

    def hide_button(self, letter: str) -> None:
        for button in self.buttons:
            if button.letter == letter:
                button.hidden = True

    def parse_data(self, data: str) -> Any:
        user_is_supervisor = api.authentication.is_supervisor()
        for button in self.buttons:
            if button.supervisor and not user_is_supervisor:
                continue

            if not button.hidden and button.letter == data:
                return button.function()

        return self.parse_input(data)

    def parse_input(self, data: str) -> Any:
        pass

    def reset(self) -> None:
        for button in self.buttons:
            button.hidden = False

    def _get_boundary(self) -> str:
        line = "-" * (self.WINDOW_SIZE - 2)
        return "+" + line + "+"

    def centered(self, text: str) -> None:
        print(f"|{text.center(self.WINDOW_SIZE - 2)}|")

    def padded(self, text: str, padding: int = 10) -> None:
        string = "|"
        string += " " * padding
        string += text
        if len(string) > self.WINDOW_SIZE:
            string = string[0 : self.WINDOW_SIZE - 2]  # noqa: E203
        string += " " * (self.WINDOW_SIZE - len(string) - 1)
        string += "|"
        print(string)

    def boundary(self) -> None:
        print(self._get_boundary())

    def empty(self) -> None:
        print("|" + " " * (self.WINDOW_SIZE - 2) + "|")

    def clear_screen(self) -> None:
        print("\n" * 5)

    def get_input(self, text: str = "Enter Command: ") -> str:
        print()
        return input(text).strip()

    def back(self) -> BACK:
        return BACK
